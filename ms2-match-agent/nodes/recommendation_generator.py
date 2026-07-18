"""
nodes/recommendation_generator.py

The recommendation-generating node in the Applytic LangGraph workflow.
Reads the results the skill_matcher node already wrote to state
(matched_skills, missing_skills, match_score) and turns them into a
list of human-readable recommendations, written back onto
state["recommendations"].

This node produces no new analysis of its own — it doesn't decide
what's matched or missing, it only turns numbers and lists that
already exist into advice a candidate can act on. That's why it needs
nothing beyond pure Python: no AI call, no external service, just
straightforward rules applied to data the graph has already computed.
"""

from state.resume_state import ResumeState

def _get_score_band_message(match_score: float) -> str:
    """
    Returns the single overall-assessment message for the given
    match_score, based on which band it falls into.

    Bands are checked from highest to lowest so each condition only
    needs a lower bound — a score of exactly 90 satisfies both
    `>= 90` and (hypothetically) `>= 70`, but because we check `>= 90`
    first and return immediately, it can never fall through and get
    double-classified into a lower band.
    """
    if match_score >= 90:
       
        return "Excellent match. Resume is ready."

    elif match_score >= 70:
      
        return "Good match. Consider improving missing skills."

    elif match_score >= 40:
       
        return "Moderate match. Learn missing skills and add relevant projects."

    else:
       
        return "Low match. Improve resume, learn required technologies, and build projects."


def _get_missing_skill_recommendations(missing_skills: list[str]) -> list[str]:
    """
    Returns one "Learn {skill}." recommendation per entry in
    missing_skills, or a single "No missing skills found." message if
    the list is empty.

    Kept as its own function (rather than inlined into
    generate_recommendations) for the same reason as
    _get_score_band_message above: this logic only depends on
    missing_skills, so it can be reasoned about and tested in
    isolation from the score-band logic.
    """
   
    if not missing_skills:
        return ["No missing skills found."]

    return [f"Learn {skill}." for skill in missing_skills]

def generate_recommendations(state: ResumeState) -> ResumeState:
    """
    Reads matched_skills, missing_skills, and match_score from state,
    and writes a combined list of recommendations back onto
    state["recommendations"].

    Args:
        state: The current ResumeState. Must already have
            match_score and missing_skills populated by the
            skill_matcher node earlier in the graph.

    Returns:
        The same ResumeState object, mutated in place with
        recommendations set — consistent with skill_matcher.py's
        match_skills(), this node updates the existing state dict
        rather than building and returning a new one.
    """

   
    match_score = state.get("match_score", 0.0)
    missing_skills = state.get("missing_skills", []) or []

    score_band_message = _get_score_band_message(match_score)

    skill_messages = _get_missing_skill_recommendations(missing_skills)

    recommendations: list[str] = [score_band_message, *skill_messages]
   
    state["recommendations"] = recommendations

    return state