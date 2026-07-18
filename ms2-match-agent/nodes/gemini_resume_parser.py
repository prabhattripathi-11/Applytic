"""
Gemini resume parser.

Takes plain resume text (already extracted by pdf_extractor.py — this
module has no idea a PDF was ever involved) and returns it as a
structured Python dictionary. Nothing in this file touches FastAPI,
LangGraph, or PDFs. Its only job: text in, structured JSON out.
"""

import json
import logging
from typing import Any

from google.genai import types
from pydantic import BaseModel, Field, ValidationError

from services.gemini_client import get_gemini_client, GEMINI_MODEL
from state.resume_state import ResumeState
from utils.pdf_extractor import extract_text_from_pdf

logger = logging.getLogger(__name__)

class ResumeParsingError(Exception):
    """Base exception for everything this module can raise."""


class GeminiResponseError(ResumeParsingError):
    """Raised when the call to Gemini itself fails (network, auth, API error)."""


class InvalidResumeJSONError(ResumeParsingError):
    """
    Raised when Gemini responded, but the response either wasn't valid
    JSON or didn't match the resume schema we require.
    """

class EducationEntry(BaseModel):
    degree: str = ""
    institution: str = ""
    start_year: str = ""
    end_year: str = ""


class ExperienceEntry(BaseModel):
    role: str = ""
    company: str = ""
    start_date: str = ""
    end_date: str = ""
    description: str = ""


class ProjectEntry(BaseModel):
    name: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)


class CertificationEntry(BaseModel):
    name: str = ""
    issuer: str = ""
    date: str = ""


class ParsedResume(BaseModel):
    """The full structured shape this module guarantees on success."""

    full_name: str = ""
    email: str = ""
    phone: str = ""
    summary: str = ""
    skills: list[str] = Field(default_factory=list)
    education: list[EducationEntry] = Field(default_factory=list)
    experience: list[ExperienceEntry] = Field(default_factory=list)
    projects: list[ProjectEntry] = Field(default_factory=list)
    certifications: list[CertificationEntry] = Field(default_factory=list)

def _build_prompt(resume_text: str) -> str:
    """
    Builds the instruction Gemini receives alongside the resume text.

    Kept as its own function (rather than an inline string in
    parse_resume_text) so the prompt can be read, tuned, and tested on
    its own — prompt wording is exactly the kind of thing that gets
    iterated on repeatedly once this is in real use.
    """
    return (
        "You are a precise resume-parsing engine. Extract structured "
        "information from the resume text below.\n\n"
        "Rules:\n"
        "- Return ONLY JSON matching the required schema. No markdown, "
        "no code fences, no commentary before or after.\n"
        "- If a field is not present in the resume, return an empty "
        "string (or empty array for list fields) — never invent or "
        "guess information that isn't in the text.\n"
        "- Preserve names, dates, and titles exactly as written in the "
        "resume; do not reformat or normalize them.\n"
        "- 'summary' should be a brief professional summary derived "
        "from the resume content, written in third person, 1-3 "
        "sentences. If the resume has no summary/objective section, "
        "write a short one based on the experience listed.\n\n"
        f'Resume text:\n"""\n{resume_text}\n"""'
    )

def _strip_code_fences(text: str) -> str:
    """
    Removes a ```json ... ``` or ``` ... ``` wrapper if present.

    response_mime_type="application/json" (set below) should already
    stop Gemini from wrapping its answer in markdown fences, but this
    is a cheap, harmless safety net in case a future model version or
    an edge-case response includes them anyway. It only strips
    surrounding fences — it never touches the JSON content itself.
    """
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()
    return stripped

def parse_resume_text(resume_text: str) -> dict[str, Any]:
    """
    Sends resume_text to Gemini and returns a structured dictionary
    matching the ParsedResume shape.

    Args:
        resume_text: Plain extracted resume text (e.g. the output of
            pdf_extractor.extract_text_from_pdf()).

    Returns:
        A dict with keys: full_name, email, phone, summary, skills,
        education, experience, projects, certifications.

    Raises:
        ValueError: resume_text is empty or not a string.
        GeminiResponseError: the call to Gemini itself failed.
        InvalidResumeJSONError: Gemini responded, but the response
            wasn't valid JSON or didn't match the expected schema.
    """
    if not resume_text or not resume_text.strip():
        raise ValueError("resume_text must be a non-empty string")

    client = get_gemini_client()

    prompt = _build_prompt(resume_text)

    logger.info("Sending resume text to Gemini (%d characters)", len(resume_text))

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ParsedResume,
                temperature=0.1,
            ),
        )
    except Exception as exc:
        logger.error("Gemini API call failed: %s", exc)
        raise GeminiResponseError(f"Gemini API call failed: {exc}") from exc
    raw_text = response.text

    if not raw_text or not raw_text.strip():
        logger.error("Gemini returned an empty response")
        raise InvalidResumeJSONError("Gemini returned an empty response")

    cleaned_text = _strip_code_fences(raw_text)

    try:
        parsed_dict = json.loads(cleaned_text)
    except json.JSONDecodeError as exc:
        logger.error(
            "Gemini response was not valid JSON: %s | raw response: %s",
            exc,
            raw_text,
        )
        raise InvalidResumeJSONError(
            f"Gemini did not return valid JSON: {exc}"
        ) from exc

    try:
        validated = ParsedResume.model_validate(parsed_dict)
    except ValidationError as exc:
        logger.error("Gemini JSON did not match the expected resume schema: %s", exc)
        raise InvalidResumeJSONError(
            f"Gemini JSON did not match the expected resume schema: {exc}"
        ) from exc

    logger.info(
        "Successfully parsed resume for: %s (%d skills, %d experience entries)",
        validated.full_name or "unknown",
        len(validated.skills),
        len(validated.experience),
    )
    return validated.model_dump()

def parse_resume(state: ResumeState) -> ResumeState:
    """
    LangGraph node.
    Reads the PDF path from the workflow state,
    extracts text,
    parses it using Gemini,
    stores the structured result back into the state.
    """

    try:
        resume_text = extract_text_from_pdf(state["resume_path"])

        state["resume_text"] = resume_text

        state["parsed_resume"] = parse_resume_text(resume_text)

    except Exception as e:
        state["errors"].append(str(e))

    return state