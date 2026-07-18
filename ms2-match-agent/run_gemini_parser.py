"""
run_gemini_parser.py

Temporary manual test script for the full MS2 pipeline so far:
PDF file -> extracted text -> Gemini-structured JSON.

This is not a pytest suite and is not wired into main.py — it's a
throwaway script you run by hand to eyeball both stages of the
pipeline against a real file before anything gets integrated into the
FastAPI app or a LangGraph flow. Delete it (or convert it into real
pytest tests) once you've confirmed both steps work end to end.

Usage (from the project root, ms2-match-agent/):
    python run_gemini_parser.py
"""
import json
import logging
from utils.pdf_extractor import (
    extract_text_from_pdf,
    PDFExtractionError,
)

from nodes.gemini_resume_parser import (
    parse_resume_text,
    ResumeParsingError,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

SAMPLE_PDF_PATH = "sample_resume.pdf"

PREVIEW_CHAR_LIMIT = 500


def main() -> None:
    """
    Runs the full pipeline once, end to end, against SAMPLE_PDF_PATH:

        1. Extract text from the PDF.
        2. Print a preview of that text.
        3. Send the text to Gemini for structured parsing.
        4. Pretty-print the resulting JSON.

    Every stage is wrapped in its own try/except so a failure in
    Stage 2 (Gemini) is never confused with a failure in Stage 1
    (the PDF itself) — each prints a message that points at exactly
    which stage broke.
    """
    logger.info("Starting Step 1: extracting text from %s", SAMPLE_PDF_PATH)

    try:
        extracted_text = extract_text_from_pdf(SAMPLE_PDF_PATH)

    except PDFExtractionError as e:
        logger.error("PDF extraction failed: %s", e)
        print(f"\n[STEP 1 FAILED] Could not extract text from PDF: {e}")
        return

    except Exception as e:
        logger.error("Unexpected error during PDF extraction: %s", e)
        print(f"\n[STEP 1 FAILED] Unexpected error: {e}")
        return
    print("-" * 36)
    print("STEP 1: PDF TEXT EXTRACTED")
    print("-" * 36)
    print(extracted_text[:PREVIEW_CHAR_LIMIT])

    logger.info(
        "Step 1 complete: extracted %d characters total", len(extracted_text)
    )

    logger.info("Starting Step 2: sending extracted text to Gemini")
    try:
        result = parse_resume_text(extracted_text)

    except ResumeParsingError as e:
        logger.error("Gemini resume parsing failed: %s", e)
        print(f"\n[STEP 2 FAILED] Could not parse resume text: {e}")
        return

    except Exception as e:
        logger.error("Unexpected error during Gemini parsing: %s", e)
        print(f"\n[STEP 2 FAILED] Unexpected error: {e}")
        return

    logger.info("Step 2 complete: received structured JSON from Gemini")

    print("\n" + "-" * 36)
    print("STEP 2: STRUCTURED RESUME JSON")
    print("-" * 36)

    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()