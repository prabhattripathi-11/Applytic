"""
nodes/skill_matcher.py

The skill-matching node in the Applytic LangGraph workflow. Compares
the skills already extracted into state["parsed_resume"] against the
skills already extracted into state["parsed_job"], and writes the
comparison results back onto the same state .

This module does no extraction and no AI calls of its own — by the
time match_skills() runs, parsed_resume and parsed_job are assumed to
already be populated by earlier nodes (the Gemini-backed resume and
job parsers). This node is pure comparison logic, which is exactly why
it needs nothing beyond the Python standard library.
"""

from state.resume_state import ResumeState


def match_skills(state: ResumeState) -> ResumeState:
    """
    Compares parsed_resume's skills against parsed_job's
    required_skills, and writes matched_skills, missing_skills, and
    match_score back onto the given state.

    Args:
        state: The current ResumeState. Must already have
            state["parsed_resume"]["skills"] and
            state["parsed_job"]["required_skills"] populated by
            earlier nodes in the graph.

    Returns:
        The same ResumeState object, mutated in place with
        matched_skills, missing_skills, and match_score set —
        per requirement 9, this node updates the existing state dict
        rather than building and returning a new one.
    """

    resume_skills = state.get("parsed_resume", {}).get("skills", []) or []
    required_skills = state.get("parsed_job", {}).get("required_skills", []) or []


    resume_skills_lookup = {
        skill.strip().lower() for skill in resume_skills if isinstance(skill, str)
    }

   
    matched_skills: list[str] = []
    missing_skills: list[str] = []

    for required_skill in required_skills:
        if not isinstance(required_skill, str):
          
            continue

        if required_skill.strip().lower() in resume_skills_lookup:
            matched_skills.append(required_skill)
        else:
            missing_skills.append(required_skill)


    if len(required_skills) == 0:
        match_score = 0.0
    else:
        match_score = round((len(matched_skills) / len(required_skills)) * 100, 2)


    state["matched_skills"] = matched_skills
    state["missing_skills"] = missing_skills
    state["match_score"] = match_score

    return state