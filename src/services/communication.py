"""
Communication Service
API requests to backend and scraper services
"""

import httpx
from typing import Dict, List, Any, Optional
from src.config.settings import settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class CommunicationService:
    """
    Handles communication with other microservices
    """
    
    def __init__(self):
        self.backend_url = settings.BACKEND_URL
        self.scraper_url = settings.SCRAPER_URL
        self.timeout = settings.REQUEST_TIMEOUT
    
    async def send_to_backend(
        self,
        endpoint: str,
        data: Dict[str, Any],
        method: str = "POST"
    ) -> Dict[str, Any]:
        """
        Send data to backend service
        
        Args:
            endpoint: API endpoint
            data: Data to send
            method: HTTP method
            
        Returns:
            Response data
        """
        try:
            url = f"{self.backend_url}{endpoint}"
            logger.info(f"Sending {method} request to backend: {url}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                if method.upper() == "POST":
                    response = await client.post(url, json=data)
                elif method.upper() == "GET":
                    response = await client.get(url, params=data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Backend request failed with status {e.response.status_code}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error communicating with backend: {str(e)}")
            raise
    
    async def request_scraping(
        self,
        query: str,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Request scraper service to scrape papers
        
        Args:
            query: Search query
            max_results: Maximum number of results to retrieve
            
        Returns:
            List of scraped papers
        """
        try:
            url = f"{self.scraper_url}/scrape"
            logger.info(f"Requesting scraper to scrape: {query}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    json={
                        "query": query,
                        "max_results": max_results
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                papers = result.get("papers", [])
                logger.info(f"Received {len(papers)} papers from scraper")
                return papers
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Scraper request failed with status {e.response.status_code}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error communicating with scraper: {str(e)}")
            raise
    
    async def notify_backend(
        self,
        request_id: str,
        status: str,
        data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Notify backend about processing status
        
        Args:
            request_id: Request identifier
            status: Processing status
            data: Optional result data
            
        Returns:
            Success status
        """
        try:
            url = f"{self.backend_url}/api/notifications"
            
            payload = {
                "request_id": request_id,
                "status": status,
                "service": "ai-service"
            }
            
            if data:
                payload["data"] = data
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                
            logger.info(f"Notified backend about request {request_id}: {status}")
            return True
            
        except Exception as e:
            logger.error(f"Error notifying backend: {str(e)}")
            return False
    
    async def health_check_backend(self) -> bool:
        """Check if backend service is healthy"""
        try:
            url = f"{self.backend_url}/health"
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Backend health check failed: {str(e)}")
            return False
    
    async def health_check_scraper(self) -> bool:
        """Check if scraper service is healthy"""
        try:
            url = f"{self.scraper_url}/health"
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Scraper health check failed: {str(e)}")
            return False
