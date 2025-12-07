"""
LLM Prompt Templates
Contains templates for different LLM tasks
"""


class PromptTemplates:
    """
    Collection of prompt templates for LLM interactions
    """
    
    @staticmethod
    def get_summary_prompt(query: str, papers_text: str) -> str:
        """
        Generate prompt for summarizing research papers
        
        Args:
            query: User's research query
            papers_text: Formatted text of research papers
            
        Returns:
            Summary prompt
        """
        return f"""
You are a research assistant helping to summarize academic papers.

User's Research Query: {query}

Research Papers:
{papers_text}

Task: Provide a comprehensive summary of these research papers in the context of the user's query.
Focus on:
1. Main findings and contributions
2. Methodologies used
3. Key results and conclusions
4. Relevance to the user's query

Keep the summary concise but informative (300-500 words).
"""
    
    @staticmethod
    def get_gaps_prompt(query: str, papers_text: str) -> str:
        """
        Generate prompt for identifying research gaps
        
        Args:
            query: User's research query
            papers_text: Formatted text of research papers
            
        Returns:
            Research gaps prompt
        """
        return f"""
You are a research analyst identifying gaps in current research.

User's Research Query: {query}

Research Papers:
{papers_text}

Task: Identify and list the research gaps based on these papers.
Consider:
1. Areas not adequately addressed
2. Limitations mentioned by authors
3. Future research directions suggested
4. Missing perspectives or methodologies
5. Contradictions or inconsistencies in findings

Provide 5-7 specific research gaps as a numbered list.
Each gap should be clear, specific, and actionable.
"""
    
    @staticmethod
    def get_simplified_explanation_prompt(
        query: str,
        summary: str,
        education_level: str
    ) -> str:
        """
        Generate prompt for simplified explanation
        
        Args:
            query: User's research query
            summary: Research summary
            education_level: User's education level
            
        Returns:
            Simplified explanation prompt
        """
        level_descriptions = {
            "high_school": "a high school student with basic knowledge",
            "undergraduate": "an undergraduate student with foundational knowledge",
            "graduate": "a graduate student with advanced knowledge",
            "phd": "a PhD researcher with expert-level knowledge",
            "general": "a general audience with no specialized knowledge"
        }
        
        audience = level_descriptions.get(education_level, "an undergraduate student")
        
        return f"""
You are an educator explaining research concepts.

User's Research Query: {query}

Research Summary:
{summary}

Target Audience: {audience}

Task: Explain the research findings in a way that {audience} can understand.

Guidelines:
1. Use appropriate language complexity for the education level
2. Include relevant examples or analogies
3. Avoid jargon unless it's appropriate for the level (then define it)
4. Focus on practical implications and real-world applications
5. Keep it engaging and accessible

Provide a clear, educational explanation (200-300 words).
"""
    
    @staticmethod
    def get_comparison_prompt(papers_text: str) -> str:
        """
        Generate prompt for comparing multiple papers
        
        Args:
            papers_text: Formatted text of research papers
            
        Returns:
            Comparison prompt
        """
        return f"""
You are a research analyst comparing academic papers.

Research Papers:
{papers_text}

Task: Compare and contrast these research papers.
Focus on:
1. Similarities in methodology and approach
2. Differences in findings and conclusions
3. Complementary insights
4. Contradictions or conflicts
5. Evolution of ideas across different publications

Provide a structured comparison highlighting key similarities and differences.
"""
    
    @staticmethod
    def get_citation_analysis_prompt(papers_text: str) -> str:
        """
        Generate prompt for analyzing citation patterns
        
        Args:
            papers_text: Formatted text of research papers
            
        Returns:
            Citation analysis prompt
        """
        return f"""
You are a research analyst examining citation patterns and research impact.

Research Papers:
{papers_text}

Task: Analyze the citation patterns and research impact.
Consider:
1. Influential papers in the field
2. Common citations across papers
3. Research trends based on publication years
4. Key authors and research groups
5. Emerging vs. established research areas

Provide insights about the research landscape and key contributors.
"""
