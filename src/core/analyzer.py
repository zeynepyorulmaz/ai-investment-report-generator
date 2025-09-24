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

        Please conduct a comprehensive analysis of the following companies: {companies}

        For each company, provide:
        1. Current market position and financial metrics
        2. Recent performance and analyst recommendations
        3. Industry trends and competitive landscape
        4. Risk factors and growth potential
        5. News impact and market sentiment
        
        Companies to analyze: {companies}
        """)
        
        result = self.agents.stock_analyst.do(analysis_task, model=self.agents.get_model_config())
        analysis_text = str(result)
        
        # Parse the result into structured format
        market_analysis = self._extract_section(analysis_text, "Market Analysis")
        financial_metrics = self._extract_section(analysis_text, "Financial Metrics")
        risk_assessment = self._extract_section(analysis_text, "Risk Assessment")
        recommendations = self._extract_section(analysis_text, "Recommendations")
        
        return StockAnalysisResult(
            company_symbols=companies,
            market_analysis=market_analysis,
            financial_metrics=financial_metrics,
            risk_assessment=risk_assessment,
            recommendations=recommendations
        )
    
    async def _rank_investments(self, stock_analysis: StockAnalysisResult) -> InvestmentRanking:
        """Phase 2: Investment potential ranking"""
        ranking_task = Task(f"""
        Based on the comprehensive stock analysis below, please rank these specific companies by investment potential: {stock_analysis.company_symbols}
        
        COMPANIES TO RANK: {stock_analysis.company_symbols}
        
        STOCK ANALYSIS:
        - Market Analysis: {stock_analysis.market_analysis}
        - Financial Metrics: {stock_analysis.financial_metrics}
        - Risk Assessment: {stock_analysis.risk_assessment}
        - Initial Recommendations: {stock_analysis.recommendations}
        
        IMPORTANT: Use the actual company names/symbols ({stock_analysis.company_symbols}) in your ranking, not generic Company A/B/C labels.
        
        Please provide:
        1. Detailed ranking of companies from best to worst investment potential
        2. Investment rationale for each company
        3. Risk evaluation and mitigation strategies
        4. Growth potential assessment
        """)
        
        result = self.agents.research_analyst.do(ranking_task, model=self.agents.get_model_config())
        ranking_text = str(result)
        
        ranked_companies = self._extract_section(ranking_text, "Company Rankings")
        investment_rationale = self._extract_section(ranking_text, "Investment Rationale")
        risk_evaluation = self._extract_section(ranking_text, "Risk Evaluation")
        growth_potential = self._extract_section(ranking_text, "Growth Potential")
        
        return InvestmentRanking(
            ranked_companies=ranked_companies,
            investment_rationale=investment_rationale,
            risk_evaluation=risk_evaluation,
            growth_potential=growth_potential
        )
    
    async def _create_portfolio_allocation(self, ranking_analysis: InvestmentRanking) -> PortfolioAllocation:
        """Phase 3: Portfolio allocation strategy"""
        portfolio_task = Task(f"""
        Based on the investment ranking and analysis below, create a strategic portfolio allocation ONLY for the companies that were analyzed.
        
        CRITICAL: 
        - ONLY allocate to the companies mentioned in the ranking analysis
        - Use the actual company names from the ranking analysis, not generic Company A/B/C labels
        - Do NOT include other companies not mentioned in the analysis
        - Ensure all allocations total 100% across ONLY the analyzed companies
        
        INVESTMENT RANKING:
        - Company Rankings: {ranking_analysis.ranked_companies}
        - Investment Rationale: {ranking_analysis.investment_rationale}
        - Risk Evaluation: {ranking_analysis.risk_evaluation}
        - Growth Potential: {ranking_analysis.growth_potential}
        
        Please provide:
        1. Specific allocation percentages for each company (must total 100%)
        2. Investment thesis and strategic rationale
        3. Risk management approach
        4. Final actionable recommendations
        """)
        
        result = self.agents.investment_lead.do(portfolio_task, model=self.agents.get_model_config())
        portfolio_text = str(result)
        
        allocation_strategy = self._extract_section(portfolio_text, "Allocation Strategy")
        investment_thesis = self._extract_section(portfolio_text, "Investment Thesis")
        risk_management = self._extract_section(portfolio_text, "Risk Management")
        final_recommendations = self._extract_section(portfolio_text, "Final Recommendations")
        
        return PortfolioAllocation(
            allocation_strategy=allocation_strategy,
            investment_thesis=investment_thesis,
            risk_management=risk_management,
            final_recommendations=final_recommendations
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
                    f.write("## Market Analysis\n")
                    f.write(result.stock_analysis.market_analysis)
                    f.write("\n\n## Financial Metrics\n")
                    f.write(result.stock_analysis.financial_metrics)
                    f.write("\n\n## Risk Assessment\n")
                    f.write(result.stock_analysis.risk_assessment)
                    f.write("\n\n## Recommendations\n")
                    f.write(result.stock_analysis.recommendations)
            
            # Save ranking report
            if result.investment_ranking:
                ranking_report_path = reports_dir / "research_analyst_report.md"
                with open(ranking_report_path, "w", encoding="utf-8") as f:
                    f.write("# Investment Ranking Report\n\n")
                    f.write(f"**Analysis Date:** {result.investment_ranking.analysis_date.isoformat()}\n\n")
                    f.write("## Company Rankings\n")
                    f.write(result.investment_ranking.ranked_companies)
                    f.write("\n\n## Investment Rationale\n")
                    f.write(result.investment_ranking.investment_rationale)
                    f.write("\n\n## Risk Evaluation\n")
                    f.write(result.investment_ranking.risk_evaluation)
                    f.write("\n\n## Growth Potential\n")
                    f.write(result.investment_ranking.growth_potential)
            
            # Save portfolio report
            if result.portfolio_allocation:
                portfolio_report_path = reports_dir / "investment_report.md"
                with open(portfolio_report_path, "w", encoding="utf-8") as f:
                    f.write("# Investment Portfolio Report\n\n")
                    f.write(f"**Analysis Date:** {result.portfolio_allocation.analysis_date.isoformat()}\n\n")
                    f.write("## Allocation Strategy\n")
                    f.write(result.portfolio_allocation.allocation_strategy)
                    f.write("\n\n## Investment Thesis\n")
                    f.write(result.portfolio_allocation.investment_thesis)
                    f.write("\n\n## Risk Management\n")
                    f.write(result.portfolio_allocation.risk_management)
                    f.write("\n\n## Final Recommendations\n")
                    f.write(result.portfolio_allocation.final_recommendations)
            
            logger.info(f"Reports saved for analysis {request_id}")
            
        except Exception as e:
            logger.error(f"Failed to save reports for {request_id}: {str(e)}")
    
    def get_analysis(self, request_id: str) -> Optional[AnalysisResult]:
        """Get analysis result by request ID"""
        return self.results_cache.get(request_id)
    
    def list_analyses(self) -> Dict[str, AnalysisResult]:
        """List all cached analyses"""
        return self.results_cache.copy()
