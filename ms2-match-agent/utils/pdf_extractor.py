"""
PDF text extraction utility.

Scope, on purpose: this module knows how to turn a PDF file on disk
into one clean string of text. Nothing more. It does not know about
FastAPI, does not know about LangGraph, and does not call Gemini —
those are separate concerns that will each live in their own module
and import from this one, not the other way around. Keeping this file
single-purpose is what "clean architecture" means in practice here:
each layer only knows about the layer below it, never the layers
above or beside it.

Usage:
    from utils.pdf_extractor import extract_text_from_pdf

    text = extract_text_from_pdf("resume.pdf")
"""

import logging
from pathlib import Path

import pdfplumber

logger = logging.getLogger(__name__)

class PDFExtractionError(Exception):
    """Base exception for every error this module can raise."""

class PDFFileNotFoundError(PDFExtractionError):
    """Raised when the given file path does not exist on disk."""

class PDFCorruptedError(PDFExtractionError):
    """Raised when pdfplumber cannot open or parse the file at all."""

class EmptyPDFTextError(PDFExtractionError):
    """
    Raised when the PDF opened successfully but no extractable text
    was found on any page.

    This is deliberately its own exception, distinct from
    PDFCorruptedError: a scanned/image-only PDF is a valid, readable
    file — pdfplumber just can't pull text out of pixels. A caller
    might want to route this specific case to an OCR fallback later,
    which is a different response than "this file is broken."
    """

def _validate_file_path(file_path: str) -> Path:
    """
    Confirms the given path points to a real, non-empty file, and
    returns it as a Path object.

    Kept separate from extract_text_from_pdf() so the main function
    reads as a straight-line sequence of steps (validate, open,
    extract, clean, return) rather than mixing validation logic in
    with extraction logic.
    """
    path = Path(file_path)

    if not path.exists():
        logger.error("PDF not found at path: %s", file_path)
        raise PDFFileNotFoundError(f"No file found at path: {file_path}")

    if not path.is_file():
        logger.error("Path exists but is not a file: %s", file_path)
        raise PDFFileNotFoundError(f"Path is not a file: {file_path}")

    if path.stat().st_size == 0:
        logger.error("PDF file is empty (0 bytes): %s", file_path)
        raise PDFCorruptedError(f"File is empty: {file_path}")

    return path


def _extract_page_text(page, page_number: int) -> str:
    """
    Extracts text from a single pdfplumber page object.

    Isolated into its own function so the per-page None/empty-text
    handling (a normal, expected outcome for scanned pages) doesn't
    clutter the main extraction loop.
    """
    text = page.extract_text()

    if text is None:
        logger.warning("No extractable text found on page %d", page_number)
        return ""

    return text


def _clean_text(raw_text: str) -> str:
    """
    Normalizes the merged text into one clean string.

    "Clean" here specifically means: no leading/trailing whitespace on
    the whole document, and no run of more than two consecutive
    blank lines (PDFs frequently produce ragged extra blank lines
    between sections). This does not alter wording or structure —
    it only tidies whitespace, so nothing about the resume's actual
    content is changed.
    """
    text = raw_text.strip()
    lines = text.splitlines()
    cleaned_lines: list[str] = []
    blank_run = 0

    for line in lines:
        if line.strip() == "":
            blank_run += 1
            if blank_run <= 1:
                cleaned_lines.append("")
        else:
            blank_run = 0
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()

def extract_text_from_pdf(file_path: str) -> str:
    """
    Reads every page of the PDF at file_path and returns all extracted
    text merged into a single clean string.

    Args:
        file_path: Path to a PDF file on disk.

    Returns:
        The full extracted text of the document, whitespace-normalized.

    Raises:
        PDFFileNotFoundError: file_path doesn't exist or isn't a file.
        PDFCorruptedError: the file exists but pdfplumber can't open
            or parse it (not a valid/readable PDF).
        EmptyPDFTextError: the PDF opened fine but no page contained
            any extractable text (e.g. a scanned, image-only PDF).
    """
    path = _validate_file_path(file_path)

    logger.info("Starting text extraction: %s", path)

    page_texts: list[str] = []

    try:
        with pdfplumber.open(path) as pdf:
            total_pages = len(pdf.pages)
            logger.debug("Opened PDF with %d page(s): %s", total_pages, path)

            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = _extract_page_text(page, page_number)
                page_texts.append(page_text)

    except PDFExtractionError:
        raise
    except Exception as exc:
        logger.error("Failed to open/parse PDF %s: %s", path, exc)
        raise PDFCorruptedError(
            f"Could not open or parse PDF at {path}: {exc}"
        ) from exc

    merged_text = "\n\n".join(page_texts)
    cleaned_text = _clean_text(merged_text)

    if not cleaned_text:
        logger.warning("No extractable text found in entire PDF: %s", path)
        raise EmptyPDFTextError(
            f"No extractable text found in PDF: {path}. "
            "This usually means the file is a scanned image without "
            "a text layer."
        )

    logger.info(
        "Successfully extracted %d characters from %s (%d pages)",
        len(cleaned_text),
        path,
        total_pages,
    )

    return cleaned_text

if __name__ == "__main__":
    import sys
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    if len(sys.argv) != 2:
        print("Usage: python utils/pdf_extractor.py <path-to-pdf>")
        sys.exit(1)

    try:
        extracted = extract_text_from_pdf(sys.argv[1])
        print("\n--- Extracted text ---\n")
        print(extracted)
    except PDFExtractionError as e:
        print(f"\nExtraction failed: {e}")
        sys.exit(1)
