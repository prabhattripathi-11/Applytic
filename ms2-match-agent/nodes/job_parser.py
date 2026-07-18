"""
nodes/job_parser.py

Converts a raw job description string into structured JSON using
Gemini. This module follows the exact same architecture as
nodes/gemini_resume_parser.py — same exception pattern, same
schema-enforced JSON mode, same defense-in-depth validation — because
these two nodes are siblings in the same pipeline and should be easy
to read as a pair, not two differently-shaped modules that happen to
both call Gemini.

Nothing in this file touches FastAPI, LangGraph, or PDFs. Its only
job: job description text in, structured JSON out.
"""

import json
import logging
from typing import Any
from google.genai import types
from pydantic import BaseModel, Field, ValidationError
from services.gemini_client import get_gemini_client, GEMINI_MODEL
from state.resume_state import ResumeState

logger = logging.getLogger(__name__)

class JobParsingError(Exception):
    """Base exception for everything this module can raise."""


class GeminiJobResponseError(JobParsingError):
    """Raised when the call to Gemini itself fails (network, auth, API error)."""


class InvalidJobJSONError(JobParsingError):
    """
    Raised when Gemini responded, but the response either wasn't valid
    JSON or didn't match the expected job-description schema.
    """
class ParsedJob(BaseModel):
    """The full structured shape this module guarantees on success."""

    job_title: str = ""
    company: str = ""
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    minimum_experience: str = ""
    education: str = ""
    responsibilities: list[str] = Field(default_factory=list)
    location: str = ""
    employment_type: str = ""

def _build_prompt(job_description: str) -> str:
    """
    Builds the instruction Gemini receives alongside the job
    description text.

    Kept as its own function (rather than inlined into
    parse_job_description) so the prompt can be read, tuned, and
    tested on its own, independent of the parsing/validation logic
    around it — exactly the same reasoning as
    gemini_resume_parser.py's _build_prompt().
    """
    return (
        "You are a precise job-description-parsing engine. Extract "
        "structured information from the job posting text below.\n\n"
        "Rules:\n"
        "- Return ONLY JSON matching the required schema. No markdown, "
        "no code fences, no commentary before or after.\n"
        "- If a field is not present in the posting, return an empty "
        "string (or empty array for list fields) — never invent or "
        "guess information that isn't in the text.\n"
        "- Distinguish required_skills from preferred_skills carefully: "
        "only list a skill under required_skills if the posting states "
        "or clearly implies it is mandatory. Skills described as "
        "'nice to have', 'a plus', or 'preferred' belong in "
        "preferred_skills instead.\n"
        "- minimum_experience should capture the stated experience "
        "requirement as written (e.g. '3+ years'), not a guess.\n"
        "- Preserve job titles, company names, and locations exactly "
        "as written in the posting; do not reformat or normalize them.\n\n"
        f'Job description text:\n"""\n{job_description}\n"""'
    )

def _strip_code_fences(text: str) -> str:
    """
    Removes a ```json ... ``` or ``` ... ``` wrapper if present.

    response_mime_type="application/json" (set below) should already
    stop Gemini from wrapping its answer in markdown fences, but this
    is a cheap, harmless safety net in case a future model version or
    an edge-case response includes them anyway. It only strips
    surrounding fences — it never touches the JSON content itself.
    Identical logic to gemini_resume_parser.py's _strip_code_fences(),
    kept as its own local copy here rather than a shared import so
    this file stays fully self-contained per the task's isolation
    requirements.
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

def parse_job_description(job_description: str) -> dict[str, Any]:
    """
    Sends job_description to Gemini and returns a structured
    dictionary matching the ParsedJob shape.

    Args:
        job_description: Raw job posting text.

    Returns:
        A dict with keys: job_title, company, required_skills,
        preferred_skills, minimum_experience, education,
        responsibilities, location, employment_type.

    Raises:
        ValueError: job_description is empty or not a string.
        GeminiJobResponseError: the call to Gemini itself failed.
        InvalidJobJSONError: Gemini responded, but the response wasn't
            valid JSON or didn't match the expected schema.
    """
  
    if not job_description or not job_description.strip():
        raise ValueError("job_description must be a non-empty string")

    
    client = get_gemini_client()

    prompt = _build_prompt(job_description)

    logger.info(
        "Sending job description to Gemini (%d characters)", len(job_description)
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
           
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ParsedJob,
                temperature=0.1,
            ),
        )
    except Exception as exc:
        logger.error("Gemini API call failed: %s", exc)
        raise GeminiJobResponseError(f"Gemini API call failed: {exc}") from exc

    raw_text = response.text

    if not raw_text or not raw_text.strip():
        logger.error("Gemini returned an empty response")
        raise InvalidJobJSONError("Gemini returned an empty response")

    cleaned_text = _strip_code_fences(raw_text)

    try:
        parsed_dict = json.loads(cleaned_text)
    except json.JSONDecodeError as exc:
        logger.error(
            "Gemini response was not valid JSON: %s | raw response: %s",
            exc,
            raw_text,
        )
        raise InvalidJobJSONError(
            f"Gemini did not return valid JSON: {exc}"
        ) from exc
    try:
        validated = ParsedJob.model_validate(parsed_dict)
    except ValidationError as exc:
        logger.error("Gemini JSON did not match the expected job schema: %s", exc)
        raise InvalidJobJSONError(
            f"Gemini JSON did not match the expected job schema: {exc}"
        ) from exc

    logger.info(
        "Successfully parsed job posting: %s at %s (%d required skills)",
        validated.job_title or "unknown title",
        validated.company or "unknown company",
        len(validated.required_skills),
    )
    return validated.model_dump()

def parse_job(state: ResumeState) -> ResumeState:
    """
    LangGraph node.
    Reads the job description from the workflow state,
    parses it with Gemini,
    stores the structured output back into the state.
    """

    try:
        state["parsed_job"] = parse_job_description(
            state["job_description"]
        )

    except Exception as e:
        state["errors"].append(str(e))

    return state