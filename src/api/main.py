"""FastAPI application for Investment Report Generator"""

import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ..models.schemas import (
    AnalysisRequest,
    AnalysisResult,
    AnalysisSummary,
    AnalysisStatus,
    HealthCheck,
    ErrorResponse
)
from ..services.investment_service import investment_service
from ..config.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format=settings.log_format
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered investment analysis and portfolio allocation system",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc) if settings.debug else "An unexpected error occurred"
        ).dict()
    )


@app.get("/", response_model=HealthCheck)
async def root():
    """Root endpoint with health check"""
    return HealthCheck()


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck()


@app.post("/analyses", response_model=AnalysisResult, status_code=status.HTTP_201_CREATED)
async def create_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Create a new investment analysis"""
    try:
        # Validate API key availability
        if not settings.has_any_api_key:
            raise HTTPException(
                status_code=400,
                detail="No API key configured. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable."
            )
        
        logger.info(f"Creating analysis for companies: {request.companies}")
        
        # Start analysis in background if requested
        result = await investment_service.create_analysis(request)
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to create analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analyses", response_model=List[AnalysisSummary])
async def list_analyses(
    status_filter: Optional[AnalysisStatus] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100)
):
    """List all analyses with optional filtering"""
    try:
        analyses = investment_service.list_analyses(status=status_filter, limit=limit)
        return analyses
    except Exception as e:
        logger.error(f"Failed to list analyses: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analyses/{request_id}", response_model=AnalysisResult)
async def get_analysis(request_id: str):
    """Get a specific analysis by ID"""
    try:
        result = investment_service.get_analysis(request_id)
        if not result:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get analysis {request_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/analyses/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(request_id: str):
    """Delete a specific analysis"""
    try:
        deleted = investment_service.delete_analysis(request_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Analysis not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete analysis {request_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyses/cleanup")
async def cleanup_old_analyses(days: int = Query(None, description="Number of days to keep analyses")):
    """Clean up old analyses"""
    try:
        cleaned_count = investment_service.cleanup_old_analyses(days)
        return {"message": f"Cleaned up {cleaned_count} old analyses"}
    except Exception as e:
        logger.error(f"Failed to cleanup analyses: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_service_stats():
    """Get service statistics"""
    try:
        stats = investment_service.get_service_stats()
        return stats
    except Exception as e:
        logger.error(f"Failed to get stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
