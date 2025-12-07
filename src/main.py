"""
Research Genie - AI Service Module
Main entry point for the FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import ai_routes
from src.utils.logger import setup_logger
from src.config.settings import settings

# Initialize logger
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Research Genie - AI Service",
    description="AI Service Module for processing research papers and generating insights",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI Service"])


@app.on_event("startup")
async def startup_event():
    """Execute on application startup"""
    logger.info("Starting Research Genie AI Service...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown"""
    logger.info("Shutting down Research Genie AI Service...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Research Genie - AI Service",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "ai-service"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
