"""
LLM Processor Service
Handles LLM calls (Gemini/ChatGPT) for paper analysis
"""

import json
from typing import List, Dict, Any
from src.config.settings import settings
from src.utils.prompts import PromptTemplates
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class LLMProcessor:
    """
    Processes research papers using LLM APIs (Gemini/ChatGPT)
    """
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL
        self.prompt_templates = PromptTemplates()
        
        # Initialize appropriate LLM client
        if self.provider == "gemini":
            self._init_gemini()
        elif self.provider == "openai":
            self._init_openai()
        else:
            logger.warning(f"Unknown LLM provider: {self.provider}")
    
    def _init_gemini(self):
        """Initialize Gemini API client"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
            logger.info("Gemini API client initialized")
        except ImportError:
            logger.error("Google Generative AI package not installed")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {str(e)}")
            self.client = None
    
    def _init_openai(self):
        """Initialize OpenAI API client"""
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            logger.info("OpenAI API client initialized")
        except ImportError:
            logger.error("OpenAI package not installed")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI: {str(e)}")
            self.client = None
    
    async def analyze_papers(
        self,
        query: str,
        papers: List[Any],
        education_level: str = "undergraduate"
    ) -> Dict[str, Any]:
        """
        Analyze research papers using LLM
        
        Args:
            query: User's research query
            papers: List of research papers
            education_level: User's education level
            
        Returns:
            Analysis results with summary, gaps, and explanation
        """
        try:
            logger.info(f"Analyzing {len(papers)} papers with {self.provider}")
            
            # Prepare papers data
            papers_text = self._format_papers(papers)
            
            # Generate summary
            summary = await self._generate_summary(query, papers_text)
            
            # Extract research gaps
            research_gaps = await self._extract_research_gaps(query, papers_text)
            
            # Generate simplified explanation based on education level
            simplified_explanation = await self._generate_simplified_explanation(
                query, summary, education_level
            )
            
            return {
                "summary": summary,
                "research_gaps": research_gaps,
                "simplified_explanation": simplified_explanation,
                "education_level": education_level
            }
            
        except Exception as e:
            logger.error(f"Error analyzing papers: {str(e)}")
            raise
    
    def _format_papers(self, papers: List[Any]) -> str:
        """Format papers for LLM input"""
        formatted = []
        for i, paper in enumerate(papers, 1):
            paper_dict = paper.dict() if hasattr(paper, 'dict') else paper
            formatted.append(
                f"Paper {i}:\n"
                f"Title: {paper_dict.get('title', 'N/A')}\n"
                f"Abstract: {paper_dict.get('abstract', 'N/A')}\n"
                f"Authors: {', '.join(paper_dict.get('authors', []))}\n"
                f"Year: {paper_dict.get('year', 'N/A')}\n"
            )
        return "\n\n".join(formatted)
    
    async def _generate_summary(self, query: str, papers_text: str) -> str:
        """Generate summary of research papers"""
        prompt = self.prompt_templates.get_summary_prompt(query, papers_text)
        return await self._call_llm(prompt)
    
    async def _extract_research_gaps(self, query: str, papers_text: str) -> List[str]:
        """Extract research gaps from papers"""
        prompt = self.prompt_templates.get_gaps_prompt(query, papers_text)
        response = await self._call_llm(prompt)
        
        # Parse response into list of gaps
        gaps = [gap.strip() for gap in response.split('\n') if gap.strip() and gap.strip()[0].isdigit()]
        return gaps if gaps else [response]
    
    async def _generate_simplified_explanation(
        self,
        query: str,
        summary: str,
        education_level: str
    ) -> str:
        """Generate simplified explanation based on education level"""
        prompt = self.prompt_templates.get_simplified_explanation_prompt(
            query, summary, education_level
        )
        return await self._call_llm(prompt)
    
    async def _call_llm(self, prompt: str) -> str:
        """
        Make API call to LLM
        
        Args:
            prompt: Prompt to send to LLM
            
        Returns:
            LLM response text
        """
        try:
            if self.provider == "gemini":
                return await self._call_gemini(prompt)
            elif self.provider == "openai":
                return await self._call_openai(prompt)
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
        except Exception as e:
            logger.error(f"LLM API call failed: {str(e)}")
            raise
    
    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API"""
        if not self.client:
            raise RuntimeError("Gemini client not initialized")
        
        response = self.client.generate_content(prompt)
        return response.text
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        if not self.client:
            raise RuntimeError("OpenAI client not initialized")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful research assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
