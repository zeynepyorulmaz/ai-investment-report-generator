"""Service layer for investment analysis operations"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from ..models.schemas import (
    AnalysisRequest,
    AnalysisResult,
    AnalysisSummary,
    AnalysisStatus
)
from ..core.analyzer import InvestmentAnalyzer
from ..config.settings import settings

logger = logging.getLogger(__name__)


class InvestmentService:
    """Service layer for investment analysis operations"""
    
    def __init__(self):
        self.analyzer = InvestmentAnalyzer()
    
    async def create_analysis(self, request: AnalysisRequest) -> AnalysisResult:
        """Create a new investment analysis"""
        try:
            logger.info(f"Creating analysis for companies: {request.companies}")
            result = await self.analyzer.analyze(request)
            return result
        except Exception as e:
            logger.error(f"Failed to create analysis: {str(e)}")
            raise
    
    def get_analysis(self, request_id: str) -> Optional[AnalysisResult]:
        """Get analysis by request ID"""
        try:
            return self.analyzer.get_analysis(request_id)
        except Exception as e:
            logger.error(f"Failed to get analysis {request_id}: {str(e)}")
            return None
    
    def list_analyses(self, 
                     status: Optional[AnalysisStatus] = None,
                     limit: int = 50) -> List[AnalysisSummary]:
        """List analyses with optional filtering"""
        try:
            analyses = self.analyzer.list_analyses()
            
            # Convert to summaries
            summaries = []
            for result in analyses.values():
                summary = AnalysisSummary(
                    request_id=result.request_id,
                    companies=result.companies,
                    status=result.status,
                    created_at=result.created_at,
                    completed_at=result.completed_at,
                    error_message=result.error_message
                )
                summaries.append(summary)
            
            # Filter by status if provided
            if status:
                summaries = [s for s in summaries if s.status == status]
            
            # Sort by creation date (newest first) and limit
            summaries.sort(key=lambda x: x.created_at, reverse=True)
            return summaries[:limit]
            
        except Exception as e:
            logger.error(f"Failed to list analyses: {str(e)}")
            return []
    
    def delete_analysis(self, request_id: str) -> bool:
        """Delete an analysis from cache"""
        try:
            if request_id in self.analyzer.results_cache:
                del self.analyzer.results_cache[request_id]
                logger.info(f"Deleted analysis {request_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete analysis {request_id}: {str(e)}")
            return False
    
    def cleanup_old_analyses(self, days: Optional[int] = None) -> int:
        """Clean up old analyses older than specified days"""
        try:
            days = days or settings.max_report_age_days
            cutoff_date = datetime.now() - timedelta(days=days)
            
            to_delete = []
            for request_id, result in self.analyzer.results_cache.items():
                if result.created_at < cutoff_date:
                    to_delete.append(request_id)
            
            for request_id in to_delete:
                del self.analyzer.results_cache[request_id]
            
            logger.info(f"Cleaned up {len(to_delete)} old analyses")
            return len(to_delete)
            
        except Exception as e:
            logger.error(f"Failed to cleanup old analyses: {str(e)}")
            return 0
    
    def get_service_stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        try:
            analyses = self.analyzer.list_analyses()
            
            stats = {
                "total_analyses": len(analyses),
                "status_counts": {},
                "recent_analyses": 0,
                "service_uptime": datetime.now().isoformat()
            }
            
            # Count by status
            for result in analyses.values():
                status = result.status.value
                stats["status_counts"][status] = stats["status_counts"].get(status, 0) + 1
            
            # Count recent analyses (last 24 hours)
            recent_cutoff = datetime.now() - timedelta(hours=24)
            stats["recent_analyses"] = sum(
                1 for result in analyses.values() 
                if result.created_at > recent_cutoff
            )
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get service stats: {str(e)}")
            return {"error": str(e)}


# Global service instance
investment_service = InvestmentService()
