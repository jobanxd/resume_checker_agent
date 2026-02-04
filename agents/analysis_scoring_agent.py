"""
Analysis & Scoring Agent - Resume-Job Fit Expert
"""
import logging

from agents.prompts.analysis_scoring_agent import prompts as ase_prompts
from graphs.state import ResumeAnalyzerState
from utils.llm_helper import call_llm_with_structured_output

logger = logging.getLogger(__name__)

def analyze_and_score(state: ResumeAnalyzerState) -> ResumeAnalyzerState:
    """
    Node 3: Analyze keywords, calculate match score, generate recommendations
    
    LLM Call: Use ANALYSIS_PROMPT
    Input: resume_keywords, target_keywords
    Output: matched_keywords, missing_keywords, match_score, confidence_notes, recommendations
    
    Args:
        state: Current workflow state
        
    Returns:
        ResumeAnalyzerState: Updated state
    """
    logger.info("="*50)
    logger.info("Analysis Scoring Agent")
    logger.info("="*50)
    
    try:
        resume_keywords = state.get("resume_keywords", [])
        target_keywords = state.get("target_keywords", [])
        
        # Prepare user input
        user_input = f"""
Resume Keywords: {resume_keywords}
Target Keywords: {target_keywords}
"""
        
        logger.info("Calling LLM for analysis and scoring")
        # LLM call for analysis and scoring
        llm_response = call_llm_with_structured_output(
            system_prompt=ase_prompts.ANALYSIS_PROMPT,
            user_input=user_input,
            temperature=0.0
        )
        
        # Update state
        state["matched_keywords"] = llm_response.get("matched_keywords", [])
        state["missing_keywords"] = llm_response.get("missing_keywords", [])
        state["match_score"] = llm_response.get("match_score", 0.0)
        state["confidence_notes"] = llm_response.get("confidence_notes", "")
        state["recommendations"] = llm_response.get("recommendations", [])
        state["current_step"] = "analyze_and_score"
        
        logger.info(f"Match score: {state['match_score']:.2%}")
        logger.info(f"Matched keywords ({len(state['matched_keywords'])}): {state['matched_keywords']}")
        logger.info(f"Missing keywords ({len(state['missing_keywords'])}): {state['missing_keywords']}")
        logger.info(f"Generated {len(state['recommendations'])} recommendations")
        logger.debug(f"Confidence notes: {state['confidence_notes']}")
        
    except Exception as e:
        logger.error(f"Error in analyze_and_score node: {str(e)}", exc_info=True)
        error_msg = f"Analysis and scoring error: {str(e)}"
        state["errors"] = state.get("errors", []) + [error_msg]
        state["matched_keywords"] = []
        state["missing_keywords"] = []
        state["match_score"] = 0.0
        state["confidence_notes"] = error_msg
        state["recommendations"] = []
    
    return state
