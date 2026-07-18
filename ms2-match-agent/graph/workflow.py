"""
graph/workflow.py

Assembles the five existing Applytic nodes (PDF extraction, resume
parsing, job parsing, skill matching, recommendation generation) into
a single LangGraph StateGraph, and exposes one function,
get_resume_workflow(), that returns the compiled graph ready to run.

This module does no work of its own — every node function it defines
is a thin wrapper that calls a function already implemented elsewhere
(utils/pdf_extractor.py, nodes/gemini_resume_parser.py,
nodes/job_parser.py, nodes/skill_matcher.py,
nodes/recommendation_generator.py) and maps its result onto
ResumeState. That's a deliberate clean-architecture boundary: this
file's only responsibility is wiring and ordering, not logic — if a
node's internal behavior needs to change, that change happens in its
own module, not here.
"""

import logging

from langgraph.graph import StateGraph, START, END

from state.resume_state import ResumeState

from utils.pdf_extractor import extract_text_from_pdf
from nodes.gemini_resume_parser import parse_resume_text
from nodes.job_parser import parse_job_description
from nodes.skill_matcher import match_skills
from nodes.recommendation_generator import generate_recommendations

logger = logging.getLogger(__name__)

def extract_resume_node(state: ResumeState) -> ResumeState:
    """
    Node 1: reads state["resume_path"], extracts the PDF's text via
    extract_text_from_pdf(), and writes the result to
    state["resume_text"].

    On failure, this node does not let the exception propagate and
    crash the whole graph run. Instead it appends a message to
    state["errors"] and leaves resume_text as an empty string —
    consistent with resume_state.py's documented design: a node
    hitting a recoverable error should record it and return a partial
    update, so any state already populated (there isn't any yet, at
    this first node, but this pattern is followed identically at every
    stage below) isn't lost.
    """
    try:
        extracted_text = extract_text_from_pdf(state["resume_path"])
        state["resume_text"] = extracted_text
        logger.info("extract_resume_node: extracted %d characters", len(extracted_text))
    except Exception as exc:
        logger.error("extract_resume_node failed: %s", exc)
        state["resume_text"] = ""
        state["errors"] = state.get("errors", []) + [f"PDF extraction failed: {exc}"]

    return state


def parse_resume_node(state: ResumeState) -> ResumeState:
    """
    Node 2: reads state["resume_text"], sends it to Gemini via
    parse_resume_text(), and writes the structured result to
    state["parsed_resume"].

    Guards against running at all if resume_text is empty (e.g.
    extract_resume_node already failed above) — there's no reason to
    spend a Gemini API call parsing nothing, and doing so would only
    produce a second, redundant error message on top of the one
    extract_resume_node already recorded.
    """
    if not state.get("resume_text"):
        logger.warning("parse_resume_node: skipped, resume_text is empty")
        state["parsed_resume"] = {}
        state["errors"] = state.get("errors", []) + [
            "Resume parsing skipped: resume_text was empty"
        ]
        return state

    try:
        parsed = parse_resume_text(state["resume_text"])
        state["parsed_resume"] = parsed
        logger.info("parse_resume_node: parsed resume successfully")
    except Exception as exc:
        logger.error("parse_resume_node failed: %s", exc)
        state["parsed_resume"] = {}
        state["errors"] = state.get("errors", []) + [f"Resume parsing failed: {exc}"]

    return state


def parse_job_node(state: ResumeState) -> ResumeState:
    """
    Node 3: reads state["job_description"], sends it to Gemini via
    parse_job_description(), and writes the structured result to
    state["parsed_job"].

    Independent of parse_resume_node's success or failure —
    job_description is part of the original input to the graph (like
    resume_path), not something produced by an earlier node, so this
    node can run regardless of what happened to the resume side of
    the pipeline.
    """
    if not state.get("job_description"):
        logger.warning("parse_job_node: skipped, job_description is empty")
        state["parsed_job"] = {}
        state["errors"] = state.get("errors", []) + [
            "Job parsing skipped: job_description was empty"
        ]
        return state

    try:
        parsed = parse_job_description(state["job_description"])
        state["parsed_job"] = parsed
        logger.info("parse_job_node: parsed job description successfully")
    except Exception as exc:
        logger.error("parse_job_node failed: %s", exc)
        state["parsed_job"] = {}
        state["errors"] = state.get("errors", []) + [f"Job parsing failed: {exc}"]

    return state


def skill_match_node(state: ResumeState) -> ResumeState:
    """
    Node 4: calls match_skills(state) directly.

    No wrapping needed here — match_skills() already takes a
    ResumeState and returns the same ResumeState, mutated in place
    (matched_skills, missing_skills, match_score), which is exactly
    the shape a LangGraph node function requires. Its own internal
    defensive handling (missing parsed_resume/parsed_job keys,
    division-by-zero on an empty required_skills list) already covers
    the failure modes this node would otherwise need to guard against,
    so this wrapper stays a direct passthrough rather than duplicating
    that logic.
    """
    return match_skills(state)


def recommendation_node(state: ResumeState) -> ResumeState:
    """
    Node 5: calls generate_recommendations(state) directly.

    Same reasoning as skill_match_node above — generate_recommendations()
    already matches the node shape LangGraph expects, and already
    handles a missing match_score/missing_skills defensively, so this
    is a direct passthrough rather than an additional wrapper layer.
    """
    return generate_recommendations(state)

def get_resume_workflow():
    """
    Builds and compiles the full Applytic LangGraph workflow, and
    returns the compiled graph ready to invoke.

    The graph is a single straight-line pipeline — no branching, no
    conditional edges — because every stage genuinely depends on the
    one before it: skill matching needs both parsed_resume and
    parsed_job, and recommendations need the matching results. There's
    no point in the current workflow where the graph needs to decide
    between multiple possible next steps.

    Returns:
        A compiled LangGraph graph. Call .invoke(initial_state) on the
        return value to run the full pipeline against a starting
        ResumeState.
    """
  
    graph_builder = StateGraph(ResumeState)

    graph_builder.add_node("extract_resume_node", extract_resume_node)
    graph_builder.add_node("parse_resume_node", parse_resume_node)
    graph_builder.add_node("parse_job_node", parse_job_node)
    graph_builder.add_node("skill_match_node", skill_match_node)
    graph_builder.add_node("recommendation_node", recommendation_node)

 
    graph_builder.add_edge(START, "extract_resume_node")

   
    graph_builder.add_edge("extract_resume_node", "parse_resume_node")
    graph_builder.add_edge("parse_resume_node", "parse_job_node")
    graph_builder.add_edge("parse_job_node", "skill_match_node")
    graph_builder.add_edge("skill_match_node", "recommendation_node")

   
    graph_builder.add_edge("recommendation_node", END)

    compiled_graph = graph_builder.compile()

    return compiled_graph

    resume_workflow = get_resume_workflow()