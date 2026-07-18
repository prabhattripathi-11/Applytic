"""
schemas/response.py

Response schema for the resume-matching endpoint. Describes exactly
what the API hands back once a ResumeMatchRequest has been processed
through the LangGraph workflow: the computed match score, the skill
breakdown, recommendations, the structured resume data, and any
errors collected along the way.

This file is intentionally independent of FastAPI, for the same
reason as schemas/request.py: a Pydantic model is a data contract, not
a web-framework detail. Keeping it free of FastAPI imports means this
same response shape can be constructed and validated in a test script,
a CLI tool, or anywhere else that needs it — not only inside a route
handler.
"""

from pydantic import BaseModel, ConfigDict, Field


class ResumeMatchResponse(BaseModel):
    """
    Output contract for a completed resume-matching run.

    Every field has a default, which is deliberate: this model is
    meant to represent the *outcome* of a workflow run, and a workflow
    run can partially fail (see errors below) without every field
    having been populated. A response missing, say, recommendations
    because an earlier node failed should still be a valid
    ResumeMatchResponse — not a validation error on top of an already
    partial result.
    """
    model_config = ConfigDict(from_attributes=True)

    match_score: float = Field(
        default=0.0,
        description="Overall match score between the resume and job description, 0-100.",
        examples=[76.92],
    )

    matched_skills: list[str] = Field(
        default_factory=list,
        description="Skills required by the job that were found in the resume.",
        examples=[["Python", "FastAPI"]],
    )

    missing_skills: list[str] = Field(
        default_factory=list,
        description="Skills required by the job that were not found in the resume.",
        examples=[["AWS", "Docker"]],
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Human-readable suggestions for improving the resume's match.",
        examples=[["Learn AWS.", "Learn Docker."]],
    )

    parsed_resume: dict = Field(
        default_factory=dict,
        description="The structured resume data extracted by the resume parser.",
        examples=[{"full_name": "Alex Candidate", "skills": ["Python", "FastAPI"]}],
    )

    errors: list[str] = Field(
        default_factory=list,
        description="Any error messages recorded while processing this request.",
        examples=[["PDF extraction failed: No file found at path: resume.pdf"]],
    )