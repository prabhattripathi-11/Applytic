"""
state/resume_state.py

Defines the shared state object that flows through the LangGraph
workflow for parsing a resume and matching it against a job
description.

This file is deliberately isolated: it imports nothing but the
standard library's `typing` module. No FastAPI, no Gemini SDK, no
pdf_extractor. That isolation is the point, not an accident — see the
"why this file has zero dependencies" note near the bottom.
"""

from typing import TypedDict

class ResumeState(TypedDict):
    """
    The complete state for the resume-parsing-and-matching workflow.

    Every field below is written by exactly one stage of the pipeline
    and read by one or more later stages. A node should only read
    fields it actually depends on and only write the fields it's
    responsible for — a node overwriting a field it doesn't own is
    usually a sign that field belongs to the wrong node, or that the
    graph's edges need rethinking.
    """
    resume_path: str
    job_description: str
    resume_text: str

    parsed_resume: dict

    parsed_job: dict

    matched_skills: list[str]

    missing_skills: list[str]

    match_score: float

    recommendations: list[str]

    errors: list[str]


