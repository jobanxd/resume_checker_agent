from typing import Optional
from pydantic import BaseModel, Field

class ResumeAnalysisRequest(BaseModel):
    """Request model for resume analysis"""
    resume_text: str = Field(..., description="Resume text content")
    job_description: str = Field(default="", description="Job description or requirements")


class ResumeAnalysisResponse(BaseModel):
    """Response model for resume analysis"""
    success: bool
    match_score: float
    matched_keywords: list[str]
    missing_keywords: list[str]
    resume_keywords: list[str]
    target_keywords: list[str]
    recommendations: list[str]
    confidence_notes: str
    final_summary: str
    validation_issues: Optional[list[str]] = None
    errors: Optional[list[str]] = None