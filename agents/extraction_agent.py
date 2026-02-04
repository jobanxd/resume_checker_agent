"""
Extraction Agent - Keyword Extraction Specialist
"""
import logging

from agents.prompts.extraction_agent import prompts as ea_prompts
from graphs.state import ResumeAnalyzerState
from utils.llm_helper import call_llm_with_structured_output

logger = logging.getLogger(__name__)

def extract_keywords(state: ResumeAnalyzerState) -> ResumeAnalyzerState:
    """
    Node 2: Extract keywords from resume and job description
    
    LLM Call: Use EXTRACTION_PROMPT
    Input: resume_text, job_description
    Output: resume_keywords, target_keywords, extraction_notes
    
    Args:
        state: Current workflow state
        
    Returns:
        ResumeAnalyzerState: Updated state
    """

    logger.info("="*50)
    logger.info("Extraction Agent")
    logger.info("="*50)
    
    try:
        resume_text = state.get("resume_text", "")
        job_description = state.get("job_description", "")
        
        # Prepare user input
        user_input = f"""
Resume Text:
{resume_text}

Job Description:
{job_description if job_description else "(No job description provided)"}
"""
        
        logger.info("Calling LLM for keyword extraction")
        # LLM call for keyword extraction
        llm_response = call_llm_with_structured_output(
            system_prompt=ea_prompts.EXTRACTION_PROMPT,
            user_input=user_input,
            temperature=0.0
        )
        
        # Update state
        state["resume_keywords"] = llm_response.get("resume_keywords", [])
        state["target_keywords"] = llm_response.get("target_keywords", [])
        state["extraction_notes"] = llm_response.get("extraction_notes", "")
        state["current_step"] = "extract_keywords"
        
        logger.info(f"Extracted {len(state['resume_keywords'])} resume keywords: {state['resume_keywords'][:5]}...")
        logger.info(f"Extracted {len(state['target_keywords'])} target keywords: {state['target_keywords'][:5]}...")
        logger.info(f"Extraction notes: {state['extraction_notes']}")
        
    except Exception as e:
        logger.error(f"Error in extract_keywords node: {str(e)}", exc_info=True)
        error_msg = f"Keyword extraction error: {str(e)}"
        state["errors"] = state.get("errors", []) + [error_msg]
        state["resume_keywords"] = []
        state["target_keywords"] = []
        state["extraction_notes"] = error_msg
    
    return state
