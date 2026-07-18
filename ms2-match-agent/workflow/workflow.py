"""
workflow/workflow.py

Assembles the four existing Resume Matching Agent nodes — resume
parsing, job description parsing, skill matching, and recommendation
generation — into a single compiled LangGraph StateGraph.

This module contains no business logic of its own. It does not parse
resumes, does not call any AI model, does not compute a match score,
and does not generate advice. Every one of those behaviors already
exists in its own node module (nodes/gemini_resume_parser.py,
nodes/job_parser.py, nodes/skill_matcher.py,
nodes/recommendation_generator.py) and is imported here unchanged.
workflow.py's only responsibility is describing the order those four
nodes run in and compiling that description into an executable graph.

Public API:
    get_resume_workflow() -> the compiled graph, ready to `.invoke()`.
"""

import logging

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from nodes.gemini_resume_parser import parse_resume
from nodes.job_parser import parse_job
from nodes.recommendation_generator import generate_recommendations
from nodes.skill_matcher import match_skills
from state.resume_state import ResumeState

logger = logging.getLogger(__name__)


def get_resume_workflow() -> CompiledStateGraph:
    """
    Builds and compiles the Resume Matching Agent's LangGraph workflow.

    The graph is a single straight-line pipeline with no branching:

        START -> parse_resume -> parse_job ->
        match_skills -> generate_recommendations -> END

    Each stage depends on the output of the one before it — skill
    matching needs both a parsed resume and a parsed job description
    already sitting in state, and recommendations need the matching
    results — so there is no point in this workflow where the graph
    needs to choose between more than one possible next step. That is
    exactly why this function uses only add_edge() (unconditional,
    one-to-one transitions) and never add_conditional_edges(): a
    conditional edge exists to let the graph choose its next node
    based on the current state, which this pipeline has no need to
    do.

    Returns:
        CompiledStateGraph: the compiled graph. Callers invoke the
        pipeline by calling `.invoke(initial_state)` on the returned
        object, where initial_state is a ResumeState with at least
        the fields the first node (parse_resume) depends on already
        populated.
    """
    logger.info("Building Resume Matching Agent workflow graph")

    graph_builder: StateGraph = StateGraph(ResumeState)

    graph_builder.add_node("parse_resume", parse_resume)
    graph_builder.add_node("parse_job", parse_job)
    graph_builder.add_node("match_skills", match_skills)
    graph_builder.add_node("generate_recommendations", generate_recommendations)

    logger.debug("Registered 4 nodes: parse_resume, parse_job, "
                 "match_skills, generate_recommendations")

    graph_builder.add_edge(START, "parse_resume")
    graph_builder.add_edge("parse_resume", "parse_job")
    graph_builder.add_edge("parse_job", "match_skills")
    graph_builder.add_edge("match_skills", "generate_recommendations")
    graph_builder.add_edge("generate_recommendations", END)

    logger.debug(
        "Wired edges: START -> parse_resume -> parse_job -> "
        "match_skills -> generate_recommendations -> END"
    )

    compiled_graph: CompiledStateGraph = graph_builder.compile()

    logger.info("Resume Matching Agent workflow graph compiled successfully")

    return compiled_graph