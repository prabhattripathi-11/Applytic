"""
Temporary manual test for pdf_extractor.py.

This is not a pytest suite and doesn't belong in the app/ package —
it's a throwaway script you run by hand to eyeball the output of
extract_text_from_pdf() against a real file. Delete it (or convert it
into a real pytest test under a tests/ folder) once you've confirmed
extraction works and move on to wiring things together.

Usage (from the project root):
    python test_pdf.py
"""
from utils.pdf_extractor import (
    extract_text_from_pdf,
    PDFExtractionError,
    PDFFileNotFoundError,
    PDFCorruptedError,
    EmptyPDFTextError,
)

SAMPLE_PDF_PATH = "sample_resume.pdf"


def main() -> None:
    """
    Runs extract_text_from_pdf() against SAMPLE_PDF_PATH and prints
    either the extracted text or a clear description of what failed.

    Wrapped in a function (instead of bare top-level code) so the
    `if __name__ == "__main__":` guard below can call it — that's a
    minor thing here, but it's the same pattern the rest of the
    project already uses in gemini_client.py, kept consistent on
    purpose.
    """
    try:
        extracted_text = extract_text_from_pdf(SAMPLE_PDF_PATH)

    except PDFFileNotFoundError as e:
        print(f"[FILE NOT FOUND] {e}")
        return

    except PDFCorruptedError as e:
        print(f"[CORRUPTED FILE] {e}")
        return

    except EmptyPDFTextError as e:
        print(f"[NO TEXT FOUND] {e}")
        return

    except PDFExtractionError as e:
        print(f"[EXTRACTION FAILED] {e}")
        return
    print("--- Extracted Text ---\n")
    print(extracted_text)
    print(f"\n--- End ({len(extracted_text)} characters) ---")
if __name__ == "__main__":
    main()