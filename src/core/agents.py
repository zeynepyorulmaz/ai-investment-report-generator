"""Investment analysis agents using Upsonic framework"""

import logging
from typing import Optional
from upsonic import Agent, Task

from ..config.settings import settings

logger = logging.getLogger(__name__)


class InvestmentAgents:
    """Factory class for creating investment analysis agents"""
    
    def __init__(self):
        self._stock_analyst: Optional[Agent] = None
        self._research_analyst: Optional[Agent] = None
        self._investment_lead: Optional[Agent] = None
    
    @property
    def stock_analyst(self) -> Agent:
        """Get or create stock analyst agent"""
        if self._stock_analyst is None:
            self._stock_analyst = Agent(
                name="Stock Analyst",
                role="Senior Investment Analyst at Goldman Sachs",
                goal="Comprehensive market analysis, financial statement evaluation, industry trend identification, news impact assessment, risk factor analysis, and growth potential evaluation",
                instructions="""
                1. Market Research 📊
                   - Analyze company fundamentals and metrics
                   - Review recent market performance
                   - Evaluate competitive positioning
                   - Assess industry trends and dynamics
                2. Financial Analysis 💹
                   - Examine key financial ratios
                   - Review analyst recommendations
                   - Analyze recent news impact
                   - Identify growth catalysts
                3. Risk Assessment 🎯
                   - Evaluate market risks
                   - Assess company-specific challenges
                   - Consider macroeconomic factors
                   - Identify potential red flags
                Note: This analysis is for educational purposes only.
                """
            )
            logger.info("Created Stock Analyst agent")
        return self._stock_analyst
    
    @property
    def research_analyst(self) -> Agent:
        """Get or create research analyst agent"""
        if self._research_analyst is None:
            self._research_analyst = Agent(
                name="Research Analyst",
                role="Senior Research Analyst at Goldman Sachs",
                goal="Investment opportunity evaluation, comparative analysis, risk-reward assessment, growth potential ranking, and strategic recommendations",
                instructions="""
                1. Investment Analysis 🔍
                   - Evaluate each company's potential
                   - Compare relative valuations
                   - Assess competitive advantages
                   - Consider market positioning
                2. Risk Evaluation 📈
                   - Analyze risk factors
                   - Consider market conditions
                   - Evaluate growth sustainability
                   - Assess management capability
                3. Company Ranking 🏆
                   - Rank based on investment potential
                   - Provide detailed rationale
                   - Consider risk-adjusted returns
                   - Explain competitive advantages
                """
            )
            logger.info("Created Research Analyst agent")
        return self._research_analyst
    
    @property
    def investment_lead(self) -> Agent:
        """Get or create investment lead agent"""
        if self._investment_lead is None:
            self._investment_lead = Agent(
                name="Investment Lead",
                role="Senior Investment Lead at Goldman Sachs",
                goal="Portfolio strategy development, asset allocation optimization, risk management, investment rationale articulation, and client recommendation delivery",
                instructions="""
                1. Portfolio Strategy 💼
                   - Develop allocation strategy
                   - Optimize risk-reward balance
                   - Consider diversification
                   - Set investment timeframes
                2. Investment Rationale 📝
                   - Explain allocation decisions
                   - Support with analysis
                   - Address potential concerns
                   - Highlight growth catalysts
                3. Recommendation Delivery 📊
                   - Present clear allocations
                   - Explain investment thesis
                   - Provide actionable insights
                   - Include risk considerations
                """
            )
            logger.info("Created Investment Lead agent")
        return self._investment_lead
    
    def get_model_config(self) -> str:
        """Get the configured model for agents"""
        return settings.default_model
