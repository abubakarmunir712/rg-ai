"""
Query Refiner Service
Optional query cleaner and preprocessor
"""

import re
from typing import Optional
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class QueryRefiner:
    """
    Refines and preprocesses user queries for better search results
    """
    
    def __init__(self):
        self.stop_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
            'what', 'how', 'where', 'when', 'why', 'which'
        }
    
    async def refine(self, query: str) -> str:
        """
        Refine the user query
        
        Args:
            query: Original user query
            
        Returns:
            Refined query string
        """
        try:
            logger.info(f"Refining query: {query}")
            
            # Basic preprocessing
            refined = query.lower().strip()
            
            # Remove extra whitespace
            refined = re.sub(r'\s+', ' ', refined)
            
            # Remove special characters but keep important ones
            refined = re.sub(r'[^\w\s\-]', ' ', refined)
            
            # Remove stop words (optional - be careful not to remove important context)
            words = refined.split()
            # Only remove stop words if query is long enough
            if len(words) > 5:
                words = [w for w in words if w not in self.stop_words or len(w) > 3]
            
            refined = ' '.join(words)
            
            # Add academic keywords if not present
            refined = self._enhance_academic_context(refined)
            
            logger.info(f"Refined query: {refined}")
            return refined
            
        except Exception as e:
            logger.error(f"Error refining query: {str(e)}")
            # Return original query if refinement fails
            return query
    
    def _enhance_academic_context(self, query: str) -> str:
        """
        Enhance query with academic context if needed
        
        Args:
            query: Query to enhance
            
        Returns:
            Enhanced query
        """
        # Add research/academic keywords if the query seems too generic
        academic_keywords = ['research', 'study', 'paper', 'analysis', 'survey']
        
        has_academic_keyword = any(keyword in query for keyword in academic_keywords)
        
        if not has_academic_keyword and len(query.split()) < 8:
            query = f"{query} research"
        
        return query
    
    def extract_key_terms(self, query: str) -> list:
        """
        Extract key terms from the query
        
        Args:
            query: Query to extract terms from
            
        Returns:
            List of key terms
        """
        words = query.lower().split()
        # Filter out stop words and short words
        key_terms = [w for w in words if w not in self.stop_words and len(w) > 3]
        return key_terms
