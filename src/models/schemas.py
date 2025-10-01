"""Pydantic models for investment analysis data structures"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator


class AnalysisStatus(str, Enum):
    """Status of analysis process"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class CompanySymbol(BaseModel):
    """Individual company symbol with validation"""
    symbol: str = Field(..., min_length=1, max_length=10, description="Stock symbol")
    
    @validator('symbol')
    def validate_symbol(cls, v):
        return v.upper().strip()


class AnalysisRequest(BaseModel):
    """Request model for investment analysis"""
    companies: List[str] = Field(..., description="List of company symbols to analyze")
    message: str = Field(default="Generate comprehensive investment analysis and portfolio allocation recommendations", description="Custom analysis message")
    analysis_type: str = Field(default="comprehensive", description="Type of analysis to perform")
    
    @validator('companies')
    def validate_companies(cls, v):
        return [company.upper().strip() for company in v if company.strip()]


class StockAnalysisResult(BaseModel):
    """Structured stock analysis result"""
    company_symbols: str = Field(..., description="Comma-separated list of analyzed companies")
    market_analysis: str = Field(..., description="Market position and trends analysis")
    financial_metrics: str = Field(..., description="Key financial metrics and ratios")
    risk_assessment: str = Field(..., description="Risk factors and assessment")
    recommendations: str = Field(..., description="Investment recommendations")
    analysis_date: datetime = Field(default_factory=datetime.now, description="When the analysis was performed")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class InvestmentRanking(BaseModel):
    """Investment potential ranking result"""
    ranked_companies: str = Field(..., description="Companies ranked by investment potential")
    investment_rationale: str = Field(..., description="Rationale for investment rankings")
    risk_evaluation: str = Field(..., description="Risk evaluation for each company")
    growth_potential: str = Field(..., description="Growth potential assessment")
    analysis_date: datetime = Field(default_factory=datetime.now, description="When the ranking was performed")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PortfolioAllocation(BaseModel):
    """Portfolio allocation strategy result"""
    allocation_strategy: str = Field(..., description="Detailed allocation strategy")
    investment_thesis: str = Field(..., description="Overall investment thesis")
    risk_management: str = Field(..., description="Risk management approach")
    final_recommendations: str = Field(..., description="Final actionable recommendations")
    analysis_date: datetime = Field(default_factory=datetime.now, description="When the allocation was created")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AnalysisResult(BaseModel):
    """Complete analysis result"""
    request_id: str = Field(..., description="Unique identifier for the analysis request")
    companies: List[str] = Field(..., description="List of analyzed companies")
    status: AnalysisStatus = Field(..., description="Current status of the analysis")
    stock_analysis: Optional[StockAnalysisResult] = Field(None, description="Stock analysis results")
    investment_ranking: Optional[InvestmentRanking] = Field(None, description="Investment ranking results")
    portfolio_allocation: Optional[PortfolioAllocation] = Field(None, description="Portfolio allocation results")
    error_message: Optional[str] = Field(None, description="Error message if analysis failed")
    created_at: datetime = Field(default_factory=datetime.now, description="When the analysis was created")
    completed_at: Optional[datetime] = Field(None, description="When the analysis was completed")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AnalysisSummary(BaseModel):
    """Summary of analysis for listing purposes"""
    request_id: str
    companies: List[str]
    status: AnalysisStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class HealthCheck(BaseModel):
    """Health check response"""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "2.0.0"
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the error occurred")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
