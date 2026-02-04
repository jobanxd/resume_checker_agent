"""
Resume Analyzer Router
"""
import time
import logging

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from graphs.workflow import resume_analyzer_graph
from graphs.state import ResumeAnalyzerState
from models.resume_analyzer import ResumeAnalysisRequest, ResumeAnalysisResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/resume-analyzer",
    tags=["Resume Analyzer"]
)


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(request: ResumeAnalysisRequest):
    """
    Analyze a resume against a job description
    
    Args:
        request: ResumeAnalysisRequest containing resume text and job description
        
    Returns:
        ResumeAnalysisResponse: Analysis results
    """
    start_time = time.time()
    logger.info("=" * 100)
    logger.info("POST /api/v1/resume-analyzer/analyze - Request received")
    logger.info(f"Request - Resume length: {len(request.resume_text)} chars, Job description length: {len(request.job_description)} chars")
    
    try:
        # Create initial state
        initial_state: ResumeAnalyzerState = {
            "resume_text": request.resume_text,
            "job_description": request.job_description,
            "errors": []
        }
        
        logger.info("Invoking resume analyzer workflow")
        
        # Run the workflow
        result = resume_analyzer_graph.invoke(initial_state)
        
        # Check if validation failed
        if not result.get("is_valid", False):
            elapsed_time = time.time() - start_time
            logger.warning(f"Analysis failed validation - Elapsed time: {elapsed_time:.2f}s")
            logger.warning(f"Validation issues: {result.get('validation_issues', [])}")
            logger.info("=" * 100)
            
            return ResumeAnalysisResponse(
                success=False,
                match_score=0.0,
                matched_keywords=[],
                missing_keywords=[],
                resume_keywords=[],
                target_keywords=[],
                recommendations=[],
                confidence_notes="",
                final_summary="",
                validation_issues=result.get("validation_issues", []),
                errors=result.get("errors", [])
            )
        
        # Return successful result
        elapsed_time = time.time() - start_time
        logger.info(f"Analysis completed successfully - Elapsed time: {elapsed_time:.2f}s")
        logger.info(f"Response - Match score: {result.get('match_score', 0.0):.2%}")
        logger.info(f"Response - Matched keywords: {len(result.get('matched_keywords', []))}, Missing keywords: {len(result.get('missing_keywords', []))}")
        logger.info(f"Response - Recommendations: {len(result.get('recommendations', []))}")
        logger.info("=" * 100)
        
        return ResumeAnalysisResponse(
            success=True,
            match_score=result.get("match_score", 0.0),
            matched_keywords=result.get("matched_keywords", []),
            missing_keywords=result.get("missing_keywords", []),
            resume_keywords=result.get("resume_keywords", []),
            target_keywords=result.get("target_keywords", []),
            recommendations=result.get("recommendations", []),
            confidence_notes=result.get("confidence_notes", ""),
            final_summary=result.get("final_summary", ""),
            validation_issues=result.get("validation_issues", []),
            errors=result.get("errors", [])
        )
        
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.error(f"Analysis failed with exception - Elapsed time: {elapsed_time:.2f}s", exc_info=True)
        logger.info("=" * 100)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/analyze-file", response_model=ResumeAnalysisResponse)
async def analyze_resume_file(
    file: UploadFile = File(..., description="Resume text file (.txt)"),
    job_description: str = Form(default="", description="Job description or requirements")
):
    """
    Analyze a resume from an uploaded file against a job description
    
    Args:
        file: Uploaded resume file (.txt format)
        job_description: Job description or requirements
        
    Returns:
        ResumeAnalysisResponse: Analysis results
    """
    start_time = time.time()
    logger.info("=" * 100)
    logger.info("POST /api/v1/resume-analyzer/analyze-file - Request received")
    logger.info(f"Request - File: {file.filename}, Job description length: {len(job_description)} chars")
    
    try:
        # Validate file type
        if not file.filename.endswith(('.txt', '.md', '.text')):
            logger.warning(f"Invalid file type: {file.filename}")
            raise HTTPException(
                status_code=400,
                detail="File must be a text file (.txt, .md, .text)"
            )
        
        # Read file content
        logger.info(f"Reading file: {file.filename}")
        content = await file.read()
        resume_text = content.decode('utf-8')
        logger.info(f"File content read: {len(resume_text)} characters")
        
        # Create initial state
        initial_state: ResumeAnalyzerState = {
            "resume_text": resume_text,
            "job_description": job_description,
            "errors": []
        }
        
        logger.info("Invoking resume analyzer workflow")
        
        # Run the workflow
        result = resume_analyzer_graph.invoke(initial_state)
        
        # Check if validation failed
        if not result.get("is_valid", False):
            elapsed_time = time.time() - start_time
            logger.warning(f"Analysis failed validation - Elapsed time: {elapsed_time:.2f}s")
            logger.warning(f"Validation issues: {result.get('validation_issues', [])}")
            logger.info("=" * 100)
            
            return ResumeAnalysisResponse(
                success=False,
                match_score=0.0,
                matched_keywords=[],
                missing_keywords=[],
                resume_keywords=[],
                target_keywords=[],
                recommendations=[],
                confidence_notes="",
                final_summary="",
                validation_issues=result.get("validation_issues", []),
                errors=result.get("errors", [])
            )
        
        # Return successful result
        elapsed_time = time.time() - start_time
        logger.info(f"Analysis completed successfully - Elapsed time: {elapsed_time:.2f}s")
        logger.info(f"Response - Match score: {result.get('match_score', 0.0):.2%}")
        logger.info(f"Response - Matched keywords: {len(result.get('matched_keywords', []))}, Missing keywords: {len(result.get('missing_keywords', []))}")
        logger.info(f"Response - Recommendations: {len(result.get('recommendations', []))}")
        logger.info("=" * 100)
        
        return ResumeAnalysisResponse(
            success=True,
            match_score=result.get("match_score", 0.0),
            matched_keywords=result.get("matched_keywords", []),
            missing_keywords=result.get("missing_keywords", []),
            resume_keywords=result.get("resume_keywords", []),
            target_keywords=result.get("target_keywords", []),
            recommendations=result.get("recommendations", []),
            confidence_notes=result.get("confidence_notes", ""),
            final_summary=result.get("final_summary", ""),
            validation_issues=result.get("validation_issues", []),
            errors=result.get("errors", [])
        )
        
    except UnicodeDecodeError:
        elapsed_time = time.time() - start_time
        logger.error(f"File encoding error - Elapsed time: {elapsed_time:.2f}s")
        logger.info("=" * 100)
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")
    except Exception as e:
        elapsed_time = time.time() - start_time
        logger.error(f"Analysis failed with exception - Elapsed time: {elapsed_time:.2f}s", exc_info=True)
        logger.info("=" * 100)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("GET /api/v1/resume-analyzer/health - Health check")
    return {"status": "healthy", "service": "Resume Analyzer"}
