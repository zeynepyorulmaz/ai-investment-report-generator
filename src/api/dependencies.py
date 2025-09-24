"""FastAPI dependencies for common functionality"""

import logging
from typing import Optional
from fastapi import Header, HTTPException, Depends

from ..config.settings import settings

logger = logging.getLogger(__name__)


async def verify_api_key(authorization: Optional[str] = Header(None)):
    """Verify API key if required (for future authentication)"""
    # This is a placeholder for future API key authentication
    # Currently, we rely on environment variables for LLM API keys
    return True


async def get_current_settings():
    """Dependency to get current settings"""
    return settings


def validate_companies(companies: list) -> list:
    """Validate company symbols"""
    if not companies:
        raise HTTPException(status_code=400, detail="At least one company symbol is required")
    
    if len(companies) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 companies allowed per analysis")
    
    # Clean and validate symbols
    clean_companies = []
    for company in companies:
        if not company or not isinstance(company, str):
            raise HTTPException(status_code=400, detail="Invalid company symbol")
        
        clean_symbol = company.strip().upper()
        if not clean_symbol or len(clean_symbol) > 10:
            raise HTTPException(status_code=400, detail=f"Invalid company symbol: {company}")
        
        clean_companies.append(clean_symbol)
    
    return clean_companies
