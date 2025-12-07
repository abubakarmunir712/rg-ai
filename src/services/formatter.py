"""
Output Formatter Service
Formats final AI output to structured JSON
"""

from typing import Dict, List, Any
from datetime import datetime
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class OutputFormatter:
    """
    Formats AI analysis results into structured output
    """
    
    def format_analysis(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format analysis results into structured output
        
        Args:
            analysis_result: Raw analysis results from LLM processor
            
        Returns:
            Formatted output dictionary
        """
        try:
            logger.info("Formatting analysis results")
            
            formatted = {
                "summary": analysis_result.get("summary", ""),
                "research_gaps": analysis_result.get("research_gaps", []),
                "simplified_explanation": analysis_result.get("simplified_explanation", ""),
                "education_level": analysis_result.get("education_level", "undergraduate"),
                "metadata": {
                    "processed_at": datetime.utcnow().isoformat(),
                    "version": "1.0.0"
                }
            }
            
            # Validate output
            self._validate_output(formatted)
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting analysis: {str(e)}")
            raise
    
    def _validate_output(self, output: Dict[str, Any]) -> bool:
        """
        Validate formatted output
        
        Args:
            output: Formatted output to validate
            
        Returns:
            True if valid
            
        Raises:
            ValueError if validation fails
        """
        required_fields = ["summary", "research_gaps", "simplified_explanation"]
        
        for field in required_fields:
            if field not in output:
                raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(output["research_gaps"], list):
            raise ValueError("research_gaps must be a list")
        
        logger.info("Output validation passed")
        return True
    
    def format_error(self, error_message: str, error_type: str = "processing_error") -> Dict[str, Any]:
        """
        Format error response
        
        Args:
            error_message: Error message
            error_type: Type of error
            
        Returns:
            Formatted error dictionary
        """
        return {
            "error": True,
            "error_type": error_type,
            "message": error_message,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def format_query_refinement(self, original: str, refined: str) -> Dict[str, Any]:
        """
        Format query refinement result
        
        Args:
            original: Original query
            refined: Refined query
            
        Returns:
            Formatted query refinement dictionary
        """
        return {
            "original_query": original,
            "refined_query": refined,
            "refined": original != refined,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def format_batch_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Format multiple analysis results
        
        Args:
            results: List of analysis results
            
        Returns:
            Formatted batch results
        """
        return {
            "total_processed": len(results),
            "results": results,
            "processed_at": datetime.utcnow().isoformat()
        }
