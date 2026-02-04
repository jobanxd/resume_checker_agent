"""
LangGraph Workflow Definition for Resume Analyzer
"""
import logging

from langgraph.graph import StateGraph, END

from graphs.state import ResumeAnalyzerState
from agents.resume_analyzer_agent import validate_input, format_output
from agents.extraction_agent import extract_keywords
from agents.analysis_scoring_agent import analyze_and_score

logger = logging.getLogger(__name__)


def should_continue(state: ResumeAnalyzerState) -> str:
    """
    Conditional edge to determine if workflow should continue after validation
    
    Args:
        state: Current workflow state
        
    Returns:
        str: Next node name or END
    """
    is_valid = state.get("is_valid", False)
    next_node = "extract_keywords" if is_valid else END
    
    logger.info(f"Validation result: is_valid={is_valid}, next_node={next_node}")
    
    if not is_valid:
        logger.warning(f"Workflow stopped due to validation failure: {state.get('validation_issues', [])}")
        return END
    
    return "extract_keywords"


def build_resume_analyzer_graph() -> StateGraph:
    """
    Build the Resume Analyzer LangGraph workflow
    
    Returns:
        StateGraph: Compiled workflow graph
    """
    logger.info("Building Resume Analyzer workflow graph")
    
    # Create the graph
    workflow = StateGraph(ResumeAnalyzerState)
    
    # Add nodes
    logger.debug("Adding nodes: validate_input, extract_keywords, analyze_and_score, format_output")
    workflow.add_node("validate_input", validate_input)
    workflow.add_node("extract_keywords", extract_keywords)
    workflow.add_node("analyze_and_score", analyze_and_score)
    workflow.add_node("format_output", format_output)
    
    # Add edges
    logger.debug("Setting entry point: validate_input")
    workflow.set_entry_point("validate_input")
    
    # Conditional edge after validation
    logger.debug("Adding conditional edge from validate_input")
    workflow.add_conditional_edges(
        "validate_input",
        should_continue,
        {
            "extract_keywords": "extract_keywords",
            END: END
        }
    )
    
    # Sequential edges
    logger.debug("Adding sequential edges")
    workflow.add_edge("extract_keywords", "analyze_and_score")
    workflow.add_edge("analyze_and_score", "format_output")
    workflow.add_edge("format_output", END)
    
    # Compile the graph
    logger.info("Compiling workflow graph")
    compiled_graph = workflow.compile()
    logger.info("Workflow graph compiled successfully")
    
    return compiled_graph


# Create the compiled graph instance
resume_analyzer_graph = build_resume_analyzer_graph()
