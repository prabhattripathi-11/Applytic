"""
routes/resume_routes.py

FastAPI router exposing the resume-matching endpoint: POST
/parse-resume. Accepts a ResumeMatchRequest (a resume path plus a job
description), runs it through the compiled LangGraph workflow, and
returns a ResumeMatchResponse.

This router owns exactly one responsibility: translating between the
HTTP layer and the workflow layer. It does not parse PDFs, does not
call Gemini, and does not compute skill matches itself — all of that
already happens inside the workflow this file invokes. If any of that
logic needs to change, it changes in its own module, not here.
"""

import logging

from fastapi import APIRouter, HTTPException

from schemas.request import ResumeMatchRequest
from schemas.response import ResumeMatchResponse
from workflow.workflow import get_resume_workflow

logger = logging.getLogger(__name__)

router = APIRouter()
_resume_workflow = get_resume_workflow()

@router.post("/parse-resume", response_model=ResumeMatchResponse)
def parse_resume(request: ResumeMatchRequest) -> ResumeMatchResponse:
    """
    Runs a resume through the full parsing-and-matching workflow.

    Request body (ResumeMatchRequest):
        resume_path: path to an already-uploaded resume PDF.
        job_description: full text of the job description to match
            against.

    Returns:
        A ResumeMatchResponse containing match_score, matched_skills,
        missing_skills, recommendations, parsed_resume, and errors.

        Note: a response can be returned successfully (HTTP 200) even
        if the `errors` field is non-empty — that represents a
        partial failure inside the workflow (e.g. the PDF couldn't be
        read) that the workflow itself already recovered from and
        reported, per resume_state.py's error-handling design. This
        endpoint only raises an HTTPException for failures the
        workflow could not recover from on its own.

    Raises:
        HTTPException(500): the workflow could not be invoked or
            failed in a way that produced no usable result at all.
    """
    logger.info(
        "Received /parse-resume request for resume_path=%s", request.resume_path
    )

    try:
 
        initial_state = {
            "resume_path": request.resume_path,
            "resume_text": "",
            "parsed_resume": {},
            "job_description": request.job_description,
            "parsed_job": {},
            "matched_skills": [],
            "missing_skills": [],
            "match_score": 0.0,
            "recommendations": [],
            "errors": [],
        }

        final_state = _resume_workflow.invoke(initial_state)

    except Exception as exc:
        logger.error(
            "Unexpected failure while processing /parse-resume for "
            "resume_path=%s: %s",
            request.resume_path,
            exc,
        )
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the resume match request.",
        ) from exc

    logger.info(
        "Completed /parse-resume for resume_path=%s (match_score=%s, %d error(s) recorded)",
        request.resume_path,
        final_state.get("match_score"),
        len(final_state.get("errors", [])),
    )
    return ResumeMatchResponse.model_validate(final_state)