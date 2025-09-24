"""Custom exceptions for the investment analyzer"""

from typing import Optional


class InvestmentAnalyzerError(Exception):
    """Base exception for investment analyzer"""
    
    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class ConfigurationError(InvestmentAnalyzerError):
    """Configuration-related errors"""
    pass


class AnalysisError(InvestmentAnalyzerError):
    """Analysis workflow errors"""
    pass


class AgentError(InvestmentAnalyzerError):
    """AI agent-related errors"""
    pass


class ValidationError(InvestmentAnalyzerError):
    """Data validation errors"""
    pass


class APIKeyError(ConfigurationError):
    """API key configuration errors"""
    pass


class ModelError(AgentError):
    """LLM model-related errors"""
    pass


class NetworkError(InvestmentAnalyzerError):
    """Network and connectivity errors"""
    pass


class TimeoutError(InvestmentAnalyzerError):
    """Timeout-related errors"""
    pass


class RateLimitError(InvestmentAnalyzerError):
    """Rate limiting errors"""
    pass
