"""
LangGraph State Definition for Resume Analyzer
"""
from typing import TypedDict, List, Optional, Dict, Any


class ResumeAnalyzerState(TypedDict, total=False):
    """
    State object for the Resume Analyzer workflow
    """
    # Inputs
    resume_text: str
    job_description: str
    file_path: Optional[str]  # optional, if uploading file
    
    # Validation (Resume Analyzer Agent)
    is_valid: bool
    validation_issues: List[str]
    input_type: str  # "job_description" or "role_keywords"
    extraction_plan: str
    
    # Extraction (Extraction Agent)
    resume_keywords: List[str]
    target_keywords: List[str]
    extraction_notes: str
    
    # Analysis (Analysis & Scoring Agent)
    matched_keywords: List[str]
    missing_keywords: List[str]
    match_score: float
    confidence_notes: str
    recommendations: List[str]
    
    # Final Output (Resume Analyzer Agent)
    final_summary: str
    json_output: Dict[str, Any]
    
    # Control
    current_step: str
    errors: List[str]
