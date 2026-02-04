"""
Resume Analyzer Agent - Main Orchestrator
"""
import logging

from agents.prompts.resume_analyzer_agent import prompts as ra_prompts
from graphs.state import ResumeAnalyzerState
from utils.file_parser import parse_text_file, validate_text_content
from utils.llm_helper import call_llm_with_structured_output, call_llm_with_text_output

logger = logging.getLogger(__name__)

def validate_input(state: ResumeAnalyzerState) -> ResumeAnalyzerState:
    """
    Node 1: Validate input resume and job description
    
    LLM Call: Use VALIDATOR_PROMPT
    Input: resume_text, job_description(target context)
    Output: is_valid, validation_issues, input_type, extraction_plan
    
    Args:
        state: Current workflow state
        
    Returns:
        ResumeAnalyzerState: Updated state
    """
    logger.info("="*50)
    logger.info("Resume Analyzer Agent")
    logger.info("="*50)

    try:
        # Parse file if file_path provided
        if state.get("file_path"):
            state["resume_text"] = parse_text_file(state["file_path"])
        
        # Basic validation
        resume_text = state.get("resume_text", "")
        job_description = state.get("job_description", "")
        
        is_valid, error = validate_text_content(resume_text, min_words=50)
        if not is_valid:
            state["is_valid"] = False
            state["validation_issues"] = [error]
            state["errors"] = state.get("errors", []) + [error]
            return state
        
        # LLM validation call
        user_input = f"Resume Text:\n{resume_text}\n\nJob Description:\n{job_description}"

        logger.info("Calling LLM for validation")
        llm_response = call_llm_with_structured_output(
            system_prompt=ra_prompts.VALIDATOR_PROMPT,
            user_input=user_input,
            temperature=0.0
        )
        
        # Update state
        state["is_valid"] = llm_response.get("is_valid", False)
        state["validation_issues"] = llm_response.get("issues", [])
        state["input_type"] = llm_response.get("input_type", "job_description")
        state["extraction_plan"] = llm_response.get("extraction_plan", "")
        state["current_step"] = "validate_input"
        
        logger.info(f"Validation result: is_valid={state['is_valid']}, input_type={state['input_type']}")
        
        if state["validation_issues"]:
            logger.warning(f"Validation issues: {state['validation_issues']}")
        
        if not state["is_valid"]:
            state["errors"] = state.get("errors", []) + state["validation_issues"]
        
    except Exception as e:
        logger.error(f"Error in validate_input node: {str(e)}", exc_info=True)
        state["is_valid"] = False
        state["validation_issues"] = [str(e)]
        state["errors"] = state.get("errors", []) + [f"Validation error: {str(e)}"]
    
    return state


def format_output(state: ResumeAnalyzerState) -> ResumeAnalyzerState:
    """
    Node 4: Format final output with human-readable summary
    
    LLM Call: Use FINAL_OUTPUT_PROMPT
    Input: All analysis results
    Output: final_summary, json_output
    
    Args:
        state: Current workflow state
        
    Returns:
        ResumeAnalyzerState: Updated state
    """
    logger.info("="*50)
    logger.info("Resume Analyzer Agent")
    logger.info("="*50)

    try:
        # Prepare user input
        user_input = f"""
Resume Keywords: {state.get('resume_keywords', [])}
Target Keywords: {state.get('target_keywords', [])}
Matched Keywords: {state.get('matched_keywords', [])}
Missing Keywords: {state.get('missing_keywords', [])}
Match Score: {state.get('match_score', 0.0)}
Confidence Notes: {state.get('confidence_notes', '')}
Recommendations: {state.get('recommendations', [])}
"""
        
        logger.info("Generating final summary with LLM")
        logger.info(f"Input data: match_score={state.get('match_score')}, matched={len(state.get('matched_keywords', []))}, missing={len(state.get('missing_keywords', []))}")
        
        # LLM call for final summary
        final_summary = call_llm_with_text_output(
            system_prompt=ra_prompts.FINAL_OUTPUT_PROMPT,
            user_input=user_input,
            temperature=0.3
        )
        
        # Build JSON output
        json_output = {
            "match_score": state.get("match_score", 0.0),
            "matched_keywords": state.get("matched_keywords", []),
            "missing_keywords": state.get("missing_keywords", []),
            "resume_keywords": state.get("resume_keywords", []),
            "target_keywords": state.get("target_keywords", []),
            "recommendations": state.get("recommendations", []),
            "confidence_notes": state.get("confidence_notes", ""),
            "final_summary": final_summary
        }
        
        state["final_summary"] = final_summary
        state["json_output"] = json_output
        state["current_step"] = "format_output"
        
        logger.info(f"Final summary generated: {len(final_summary)} characters")
        
    except Exception as e:
        logger.error(f"Error in format_output node: {str(e)}", exc_info=True)
        error_msg = f"Output formatting error: {str(e)}"
        state["errors"] = state.get("errors", []) + [error_msg]
        state["final_summary"] = f"Error generating summary: {str(e)}"
        state["json_output"] = {"error": error_msg}
    
    return state
