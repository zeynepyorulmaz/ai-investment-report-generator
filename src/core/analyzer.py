"""Core investment analysis workflow logic"""

import logging
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from upsonic import Task

from ..models.schemas import (
    AnalysisRequest, 
    AnalysisResult, 
    StockAnalysisResult, 
    InvestmentRanking, 
    PortfolioAllocation,
    AnalysisStatus
)
from ..config.settings import settings
from .agents import InvestmentAgents

logger = logging.getLogger(__name__)


class InvestmentAnalyzer:
    """Main investment analysis workflow orchestrator"""
    
    def __init__(self):
        self.agents = InvestmentAgents()
        self.results_cache: Dict[str, AnalysisResult] = {}
    
    async def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        """Run complete investment analysis workflow"""
        request_id = str(uuid.uuid4())
        companies_str = ", ".join(request.companies)
        
        # Initialize result
        result = AnalysisResult(
            request_id=request_id,
            companies=request.companies,
            status=AnalysisStatus.IN_PROGRESS,
            stock_analysis=None,
            investment_ranking=None,
            portfolio_allocation=None,
            error_message=None,
            completed_at=None
        )
        self.results_cache[request_id] = result
        
        logger.info(f"Starting analysis {request_id} for companies: {companies_str}")
        
        try:
            # Phase 1: Stock Analysis
            logger.info(f"Phase 1: Stock analysis for {request_id}")
            stock_analysis = await self._analyze_stocks(companies_str, request.message)
            result.stock_analysis = stock_analysis
            
            # Phase 2: Investment Ranking
            logger.info(f"Phase 2: Investment ranking for {request_id}")
            ranking_analysis = await self._rank_investments(stock_analysis)
            result.investment_ranking = ranking_analysis
            
            # Phase 3: Portfolio Allocation
            logger.info(f"Phase 3: Portfolio allocation for {request_id}")
            portfolio_strategy = await self._create_portfolio_allocation(ranking_analysis)
            result.portfolio_allocation = portfolio_strategy
            
            # Mark as completed
            result.status = AnalysisStatus.COMPLETED
            result.completed_at = datetime.now()
            
            # Save reports
            await self._save_reports(request_id, result)
            
            logger.info(f"Analysis {request_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Analysis {request_id} failed: {str(e)}")
            result.status = AnalysisStatus.FAILED
            result.error_message = str(e)
            result.completed_at = datetime.now()
        
        self.results_cache[request_id] = result
        return result
    
    async def _analyze_stocks(self, companies: str, message: str) -> StockAnalysisResult:
        """Phase 1: Comprehensive stock analysis"""
        analysis_task = Task(f"""
        {message}

        CRITICAL INSTRUCTION: You MUST analyze ONLY these specific companies using their EXACT stock symbols: {companies}

        Please conduct a comprehensive analysis of ONLY the following companies: {companies}

        For EACH of these specific companies ({companies}), provide:
        1. Current market position and financial metrics
        2. Recent performance and analyst recommendations
        3. Industry trends and competitive landscape
        4. Risk factors and growth potential
        5. News impact and market sentiment
        
        IMPORTANT: 
        - Use ONLY the company symbols provided: {companies}
        - Do NOT use generic names like "Company A", "Tech Inc.", etc.
        - Reference each company by its actual stock symbol (e.g., AAPL for Apple, MSFT for Microsoft)
        
        Companies to analyze: {companies}
        """)
        
        result = self.agents.stock_analyst.do(analysis_task, model=self.agents.get_model_config())
        analysis_text = str(result)
        
        # Use the full AI response for all fields to ensure content is preserved
        return StockAnalysisResult(
            company_symbols=companies,
            market_analysis=analysis_text,
            financial_metrics=analysis_text,
            risk_assessment=analysis_text,
            recommendations=analysis_text
        )
    
    async def _rank_investments(self, stock_analysis: StockAnalysisResult) -> InvestmentRanking:
        """Phase 2: Investment potential ranking"""
        ranking_task = Task(f"""
        Based on the comprehensive stock analysis below, please rank these EXACT companies by investment potential: {stock_analysis.company_symbols}
        
        MANDATORY: ONLY rank these specific companies: {stock_analysis.company_symbols}
        
        STOCK ANALYSIS:
        - Market Analysis: {stock_analysis.market_analysis}
        - Financial Metrics: {stock_analysis.financial_metrics}
        - Risk Assessment: {stock_analysis.risk_assessment}
        - Initial Recommendations: {stock_analysis.recommendations}
        
        CRITICAL REQUIREMENTS:
        - Use ONLY the actual company symbols: {stock_analysis.company_symbols}
        - Do NOT create fictional companies or use generic names
        - Reference each company by its stock ticker (e.g., NVDA, AMD, INTC)
        - Rank ALL and ONLY the companies listed: {stock_analysis.company_symbols}
        
        Please provide:
        1. Detailed ranking of THESE EXACT companies ({stock_analysis.company_symbols}) from best to worst investment potential
        2. Investment rationale for each of these specific companies
        3. Risk evaluation and mitigation strategies for each company
        4. Growth potential assessment for each company
        
        Remember: Analyze ONLY {stock_analysis.company_symbols} - no other companies!
        """)
        
        result = self.agents.research_analyst.do(ranking_task, model=self.agents.get_model_config())
        ranking_text = str(result)
        
        # Use the full AI response for all fields to ensure content is preserved
        return InvestmentRanking(
            ranked_companies=ranking_text,
            investment_rationale=ranking_text,
            risk_evaluation=ranking_text,
            growth_potential=ranking_text
        )
    
    async def _create_portfolio_allocation(self, ranking_analysis: InvestmentRanking) -> PortfolioAllocation:
        """Phase 3: Portfolio allocation strategy"""
        portfolio_task = Task(f"""
        Based on the investment ranking and analysis below, create a strategic portfolio allocation for EXACTLY these companies.
        
        MANDATORY CONSTRAINTS: 
        - Allocate ONLY to the companies from the ranking analysis
        - Use the EXACT company stock symbols, not generic names
        - Do NOT create or mention any other companies
        - Allocations must total EXACTLY 100%
        - Reference companies by their stock tickers (e.g., NVDA, AMD, INTC)
        
        COMPANIES TO ALLOCATE (and ONLY these):
        From the ranking analysis: {ranking_analysis.ranked_companies}
        
        INVESTMENT RANKING DATA:
        - Company Rankings: {ranking_analysis.ranked_companies}
        - Investment Rationale: {ranking_analysis.investment_rationale}
        - Risk Evaluation: {ranking_analysis.risk_evaluation}
        - Growth Potential: {ranking_analysis.growth_potential}
        
        REQUIRED OUTPUT:
        1. Specific allocation percentages for EACH company mentioned in the rankings (must total exactly 100%)
        2. Investment thesis for EACH specific company
        3. Risk management approach for the portfolio
        4. Final actionable recommendations for THESE EXACT companies
        
        IMPORTANT: Use ONLY the companies mentioned in the ranking analysis above. Do not invent new companies!
        """)
        
        result = self.agents.investment_lead.do(portfolio_task, model=self.agents.get_model_config())
        portfolio_text = str(result)
        
        # Use the full AI response for all fields to ensure content is preserved
        return PortfolioAllocation(
            allocation_strategy=portfolio_text,
            investment_thesis=portfolio_text,
            risk_management=portfolio_text,
            final_recommendations=portfolio_text
        )
    
    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract a specific section from the analysis text"""
        lines = text.split('\n')
        section_content = []
        in_section = False
        
        for line in lines:
            if section_name.lower() in line.lower() and ('##' in line or '#' in line):
                in_section = True
                continue
            elif in_section and line.strip().startswith('#'):
                break
            elif in_section:
                section_content.append(line)
        
        return '\n'.join(section_content).strip() if section_content else f"Analysis for {section_name} section"
    
    async def _save_reports(self, request_id: str, result: AnalysisResult) -> None:
        """Save analysis reports to files"""
        reports_dir = settings.reports_dir / "investment" / request_id
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Save stock analysis report
            if result.stock_analysis:
                stock_report_path = reports_dir / "stock_analyst_report.md"
                with open(stock_report_path, "w", encoding="utf-8") as f:
                    f.write("# Stock Analysis Report\n\n")
                    f.write(f"**Companies:** {result.stock_analysis.company_symbols}\n\n")
                    f.write(f"**Analysis Date:** {result.stock_analysis.analysis_date.isoformat()}\n\n")
                    f.write("## Complete Analysis\n\n")
                    f.write(result.stock_analysis.market_analysis)
                    f.write("\n\n")
            
            # Save ranking report
            if result.investment_ranking:
                ranking_report_path = reports_dir / "research_analyst_report.md"
                with open(ranking_report_path, "w", encoding="utf-8") as f:
                    f.write("# Investment Ranking Report\n\n")
                    f.write(f"**Analysis Date:** {result.investment_ranking.analysis_date.isoformat()}\n\n")
                    f.write("## Complete Ranking Analysis\n\n")
                    f.write(result.investment_ranking.ranked_companies)
                    f.write("\n\n")
            
            # Save portfolio report
            if result.portfolio_allocation:
                portfolio_report_path = reports_dir / "investment_report.md"
                with open(portfolio_report_path, "w", encoding="utf-8") as f:
                    f.write("# Investment Portfolio Report\n\n")
                    f.write(f"**Analysis Date:** {result.portfolio_allocation.analysis_date.isoformat()}\n\n")
                    f.write("## Complete Portfolio Analysis\n\n")
                    f.write(result.portfolio_allocation.allocation_strategy)
                    f.write("\n\n")
            
            logger.info(f"Reports saved for analysis {request_id}")
            
        except Exception as e:
            logger.error(f"Failed to save reports for {request_id}: {str(e)}")
    
    def get_analysis(self, request_id: str) -> Optional[AnalysisResult]:
        """Get analysis result by request ID"""
        return self.results_cache.get(request_id)
    
    def list_analyses(self) -> Dict[str, AnalysisResult]:
        """List all cached analyses"""
        return self.results_cache.copy()
