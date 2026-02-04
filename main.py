"""
FastAPI Main Application Entry Point
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.resume_analyzer import router

# Set up logging for uvicorn
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("=" * 100)
    logger.info("Starting Resume Analyzer API")
    logger.info("Application startup complete")
    logger.info("API Documentation available at: /docs")
    logger.info("=" * 100)
    
    yield
    
    # Shutdown
    logger.info("=" * 100)
    logger.info("Shutting down Resume Analyzer API")
    logger.info("=" * 100)


# Create FastAPI app
app = FastAPI(
    title="Resume Analyzer API",
    description="AI-powered resume analysis using LangGraph and OpenAI",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint"""
    logger.debug("GET / - Root endpoint accessed")
    return {
        "message": "Welcome to Resume Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    logger.debug("GET /health - Health check")
    return {"status": "healthy"}