"""
Resume Analysis Service Layer
"""
import logging

from typing import Dict, Any, Optional

from graphs.workflow import resume_analyzer_graph
from graphs.state import ResumeAnalyzerState

logger = logging.getLogger(__name__)

class ResumeAnalysisService:
    """Service for handling resume analysis operations"""
    
    def __init__(self):
        self.graph = resume_analyzer_graph
    
    def analyze_resume(
        self,
        resume_text: str,
        job_description: str = "",
        file_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a resume against a job description
        
        Args:
            resume_text: Resume content as text
            job_description: Job description or requirements
            file_path: Optional file path if analyzing from file
            
        Returns:
            Dict containing analysis results
        """
        logger.info("=" * 80)
        logger.info("Starting resume analysis")
        logger.info(f"Resume text length: {len(resume_text)} characters")
        logger.info(f"Job description length: {len(job_description)} characters")
        if file_path:
            logger.info(f"File path provided: {file_path}")
        
        # Create initial state
        initial_state: ResumeAnalyzerState = {
            "resume_text": resume_text,
            "job_description": job_description,
            "errors": []
        }
        
        if file_path:
            initial_state["file_path"] = file_path
        
        logger.info("Invoking LangGraph workflow")
        
        try:
            # Run the workflow
            result = self.graph.invoke(initial_state)
            
            logger.info("Workflow execution completed")
            logger.info(f"Final state - is_valid: {result.get('is_valid', False)}")
            logger.info(f"Final state - match_score: {result.get('match_score', 0.0):.2%}")
            logger.info(f"Final state - errors: {len(result.get('errors', []))} errors")
            logger.info("=" * 80)
            
            return result
            
        except Exception as e:
            logger.error(f"Error during workflow execution: {str(e)}", exc_info=True)
            logger.info("=" * 80)
            raise
    
    def get_analysis_summary(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key summary information from analysis result
        
        Args:
            result: Full analysis result
            
        Returns:
            Dict with summarized information
        """
        logger.debug("Extracting analysis summary")
        
        summary = {
            "is_valid": result.get("is_valid", False),
            "match_score": result.get("match_score", 0.0),
            "matched_count": len(result.get("matched_keywords", [])),
            "missing_count": len(result.get("missing_keywords", [])),
            "has_errors": len(result.get("errors", [])) > 0
        }
        
        logger.debug(f"Summary: {summary}")
        return summary


# Create singleton instance
resume_analysis_service = ResumeAnalysisService()
