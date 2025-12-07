"""
AI Service Routes
Exposes API endpoints for AI processing
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from src.services.query_refiner import QueryRefiner
from src.services.llm_processor import LLMProcessor
from src.services.formatter import OutputFormatter
from src.utils.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

# Initialize services
query_refiner = QueryRefiner()
llm_processor = LLMProcessor()
output_formatter = OutputFormatter()


# Request/Response Models
class RefineQueryRequest(BaseModel):
    query: str = Field(..., description="User's research query")
    
    
class RefineQueryResponse(BaseModel):
    original_query: str
    refined_query: str
    

class Paper(BaseModel):
    title: str
    abstract: str
    authors: Optional[List[str]] = []
    year: Optional[int] = None
    url: Optional[str] = None
    

class AnalyzePapersRequest(BaseModel):
    query: str = Field(..., description="User's research query")
    papers: List[Paper] = Field(..., description="List of research papers")
    education_level: str = Field(default="undergraduate", description="User's education level")
    

class AnalyzePapersResponse(BaseModel):
    summary: str
    research_gaps: List[str]
    simplified_explanation: str
    education_level: str


@router.post("/refine_query", response_model=RefineQueryResponse)
async def refine_query(request: RefineQueryRequest):
    """
    Refine user query before scraping
    """
    try:
        logger.info(f"Refining query: {request.query}")
        refined = await query_refiner.refine(request.query)
        
        return RefineQueryResponse(
            original_query=request.query,
            refined_query=refined
        )
    except Exception as e:
        logger.error(f"Error refining query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to refine query: {str(e)}"
        )


@router.post("/analyze_papers", response_model=AnalyzePapersResponse)
async def analyze_papers(request: AnalyzePapersRequest):
    """
    Process papers and user data to generate research gaps and insights
    """
    try:
        logger.info(f"Analyzing {len(request.papers)} papers for query: {request.query}")
        
        # Process papers through LLM
        analysis_result = await llm_processor.analyze_papers(
            query=request.query,
            papers=request.papers,
            education_level=request.education_level
        )
        
        # Format output
        formatted_output = output_formatter.format_analysis(analysis_result)
        
        return AnalyzePapersResponse(
            summary=formatted_output["summary"],
            research_gaps=formatted_output["research_gaps"],
            simplified_explanation=formatted_output["simplified_explanation"],
            education_level=request.education_level
        )
        
    except Exception as e:
        logger.error(f"Error analyzing papers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze papers: {str(e)}"
        )
