"""
schemas/request.py

Request schema for the resume-matching endpoint. Describes exactly
what a caller must send to trigger a match run: a path to an already
uploaded resume PDF, and the job description to match it against.

This file is intentionally independent of FastAPI. A Pydantic model
is just a data contract — it doesn't need to know whether it's being
populated from an HTTP request body, a test fixture, or a CLI script.
Keeping that separation means this schema can be imported and reused
anywhere a validated resume-match request is needed, not only inside
a FastAPI route.
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ResumeMatchRequest(BaseModel):
    """
    Input contract for a resume-matching request.

    Both fields are required. Validation on this model guarantees that
    by the time a ResumeMatchRequest instance exists, resume_path and
    job_description are non-empty strings — code downstream (e.g. the
    LangGraph workflow's initial state) never needs to re-check that
    itself.
    """
    model_config = ConfigDict(from_attributes=True)
    resume_path: str = Field(
        ...,
        description="Absolute or relative path of the uploaded resume PDF on disk.",
        examples=["uploads/sample_resume.pdf"],
    )

    job_description: str = Field(
        ...,
        description="Full text of the job description to match the resume against.",
        examples=[
            "Senior Backend Engineer role requiring 5+ years of Python "
            "and hands-on AWS experience."
        ],
    )
    @field_validator("resume_path")
    @classmethod
    def resume_path_must_not_be_empty(cls, value: str) -> str:
        """Rejects an empty or whitespace-only resume_path."""
        if not value.strip():
            raise ValueError("resume_path must not be empty")
        return value

    @field_validator("job_description")
    @classmethod
    def job_description_must_not_be_empty(cls, value: str) -> str:
        """Rejects an empty or whitespace-only job_description."""
        if not value.strip():
            raise ValueError("job_description must not be empty")
        return value