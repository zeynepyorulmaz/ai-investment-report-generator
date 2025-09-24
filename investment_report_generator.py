"""💰 Investment Report Generator - Your AI Financial Analysis Studio!

This advanced example demonstrates how to build a sophisticated investment analysis system that combines
market research, financial analysis, and portfolio management using the Upsonic AI Agent Framework.

The workflow uses a three-stage approach:
1. Comprehensive stock analysis and market research
2. Investment potential evaluation and ranking
3. Strategic portfolio allocation recommendations

Key capabilities:
- Real-time market data analysis
- Professional financial research
- Investment risk assessment
- Portfolio allocation strategy
- Detailed investment rationale

Example companies to analyze:
- "AAPL, MSFT, GOOGL" (Tech Giants)
- "NVDA, AMD, INTC" (Semiconductor Leaders)
- "TSLA, F, GM" (Automotive Innovation)
- "JPM, BAC, GS" (Banking Sector)
- "AMZN, WMT, TGT" (Retail Competition)
- "PFE, JNJ, MRNA" (Healthcare Focus)
- "XOM, CVX, BP" (Energy Sector)

Run `pip install upsonic requests` to install dependencies.
"""

import random
import os
from pathlib import Path
from shutil import rmtree
from typing import Dict, Any
from dataclasses import dataclass

from upsonic import Task, Agent


os.getenv('OPENAI_API_KEY')
# --- Data structures for structured outputs ---
@dataclass
class StockAnalysisResult:
    company_symbols: str
    market_analysis: str
    financial_metrics: str
    risk_assessment: str
    recommendations: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "company_symbols": self.company_symbols,
            "market_analysis": self.market_analysis,
            "financial_metrics": self.financial_metrics,
            "risk_assessment": self.risk_assessment,
            "recommendations": self.recommendations
        }


@dataclass
class InvestmentRanking:
    ranked_companies: str
    investment_rationale: str
    risk_evaluation: str
    growth_potential: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "ranked_companies": self.ranked_companies,
            "investment_rationale": self.investment_rationale,
            "risk_evaluation": self.risk_evaluation,
            "growth_potential": self.growth_potential
        }


@dataclass
class PortfolioAllocation:
    allocation_strategy: str
    investment_thesis: str
    risk_management: str
    final_recommendations: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "allocation_strategy": self.allocation_strategy,
            "investment_thesis": self.investment_thesis,
            "risk_management": self.risk_management,
            "final_recommendations": self.final_recommendations
        }


# --- Simple web search tool ---
def search_web(query: str) -> str:
    """Simple web search function for market data research"""
    try:
        # Using a simple search API (you can replace with your preferred search service)
        # For demo purposes, we'll simulate market research
        search_results = f"""
        Market Research Results for: {query}
        
        Recent Market Data:
        - Current market sentiment: Mixed with cautious optimism
        - Sector performance: Technology leading, energy volatile
        - Economic indicators: Inflation cooling, interest rates stable
        - Analyst consensus: Hold to moderate buy recommendations
        
        Key Financial Metrics:
        - P/E ratios: Generally elevated but showing normalization
        - Revenue growth: Steady across most sectors
        - Profit margins: Under pressure but stabilizing
        - Cash flows: Strong for established companies
        
        Recent News Impact:
        - Regulatory changes affecting tech sector
        - Supply chain improvements in manufacturing
        - Consumer spending patterns shifting
        - Geopolitical tensions affecting energy markets
        """
        return search_results
    except Exception as e:
        return f"Search error: {str(e)}"


# --- File management ---
reports_dir = Path(__file__).parent.joinpath("reports", "investment")
if reports_dir.is_dir():
    rmtree(path=reports_dir, ignore_errors=True)
reports_dir.mkdir(parents=True, exist_ok=True)

stock_analyst_report = str(reports_dir.joinpath("stock_analyst_report.md"))
research_analyst_report = str(reports_dir.joinpath("research_analyst_report.md"))
investment_report = str(reports_dir.joinpath("investment_report.md"))


# --- Investment Analysis Workflow Class ---
class InvestmentAnalysisWorkflow:
    def __init__(self):
        # Initialize agents with Upsonic using same descriptions as agno version
        self.stock_analyst = Agent(
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
        
        self.research_analyst = Agent(
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
        
        self.investment_lead = Agent(
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

    def analyze_stocks(self, companies: str, message: str) -> StockAnalysisResult:
        """Phase 1: Comprehensive stock analysis"""
        print("\n📊 PHASE 1: COMPREHENSIVE STOCK ANALYSIS")
        print("=" * 60)
        
        # Create task for stock analysis
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
        
        print("🔍 Analyzing market data and fundamentals...")
        result = self.stock_analyst.do(analysis_task, model="openai/gpt-4o-mini")
        
        # Parse the result into structured format
        analysis_text = str(result)
        
        # Simple parsing (in production, you'd use more sophisticated parsing)
        market_analysis = self._extract_section(analysis_text, "Market Analysis")
        financial_metrics = self._extract_section(analysis_text, "Financial Metrics")
        risk_assessment = self._extract_section(analysis_text, "Risk Assessment")
        recommendations = self._extract_section(analysis_text, "Recommendations")
        
        stock_analysis = StockAnalysisResult(
            company_symbols=companies,
            market_analysis=market_analysis,
            financial_metrics=financial_metrics,
            risk_assessment=risk_assessment,
            recommendations=recommendations
        )
        
        # Save to file
        with open(stock_analyst_report, "w") as f:
            f.write("# Stock Analysis Report\n\n")
            f.write(f"**Companies:** {stock_analysis.company_symbols}\n\n")
            f.write(str(result))
        
        print(f"✅ Stock analysis completed and saved to {stock_analyst_report}")
        return stock_analysis

    def rank_investments(self, stock_analysis: StockAnalysisResult) -> InvestmentRanking:
        """Phase 2: Investment potential ranking"""
        print("\n🏆 PHASE 2: INVESTMENT POTENTIAL RANKING")
        print("=" * 60)
        
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
        
        print("📈 Ranking companies by investment potential...")
        result = self.research_analyst.do(ranking_task, model="openai/gpt-4o-mini")
        
        # Parse the result into structured format
        ranking_text = str(result)
        
        ranked_companies = self._extract_section(ranking_text, "Company Rankings")
        investment_rationale = self._extract_section(ranking_text, "Investment Rationale")
        risk_evaluation = self._extract_section(ranking_text, "Risk Evaluation")
        growth_potential = self._extract_section(ranking_text, "Growth Potential")
        
        ranking_analysis = InvestmentRanking(
            ranked_companies=ranked_companies,
            investment_rationale=investment_rationale,
            risk_evaluation=risk_evaluation,
            growth_potential=growth_potential
        )
        
        # Save to file
        with open(research_analyst_report, "w") as f:
            f.write("# Investment Ranking Report\n\n")
            f.write(str(result))
        
        print(f"✅ Investment ranking completed and saved to {research_analyst_report}")
        return ranking_analysis

    def create_portfolio_allocation(self, ranking_analysis: InvestmentRanking) -> PortfolioAllocation:
        """Phase 3: Portfolio allocation strategy"""
        print("\n💼 PHASE 3: PORTFOLIO ALLOCATION STRATEGY")
        print("=" * 60)
        
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
        
        print("💰 Developing portfolio allocation strategy...")
        result = self.investment_lead.do(portfolio_task, model="openai/gpt-4o-mini")
        
        # Parse the result into structured format
        portfolio_text = str(result)
        
        allocation_strategy = self._extract_section(portfolio_text, "Allocation Strategy")
        investment_thesis = self._extract_section(portfolio_text, "Investment Thesis")
        risk_management = self._extract_section(portfolio_text, "Risk Management")
        final_recommendations = self._extract_section(portfolio_text, "Final Recommendations")
        
        portfolio_strategy = PortfolioAllocation(
            allocation_strategy=allocation_strategy,
            investment_thesis=investment_thesis,
            risk_management=risk_management,
            final_recommendations=final_recommendations
        )
        
        # Save to file
        with open(investment_report, "w") as f:
            f.write("# Investment Portfolio Report\n\n")
            f.write(str(result))
        
        print(f"✅ Portfolio strategy completed and saved to {investment_report}")
        return portfolio_strategy

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

    def run_complete_analysis(self, companies: str, message: str) -> str:
        """Execute the complete investment analysis workflow"""
        if not companies:
            return "❌ No company symbols provided"

        print(f"🚀 Starting investment analysis for companies: {companies}")
        print(f"💼 Analysis request: {message}")

        try:
            # Phase 1: Stock Analysis
            stock_analysis = self.analyze_stocks(companies, message)
            
            # Phase 2: Investment Ranking
            ranking_analysis = self.rank_investments(stock_analysis)
            
            # Phase 3: Portfolio Allocation
            portfolio_strategy = self.create_portfolio_allocation(ranking_analysis)
            
            # Final summary
            summary = f"""
🎉 INVESTMENT ANALYSIS WORKFLOW COMPLETED!

📊 Analysis Summary:
• Companies Analyzed: {companies}
• Market Analysis: ✅ Completed
• Investment Ranking: ✅ Completed
• Portfolio Strategy: ✅ Completed

📁 Reports Generated:
• Stock Analysis: {stock_analyst_report}
• Investment Ranking: {research_analyst_report}
• Portfolio Strategy: {investment_report}

💡 Key Insights:
{portfolio_strategy.allocation_strategy[:200]}...

⚠️ Disclaimer: This analysis is for educational purposes only and should not be considered as financial advice.
            """
            
            return summary
            
        except Exception as e:
            error_msg = f"❌ Error during analysis: {str(e)}"
            print(error_msg)
            return error_msg


# --- Main execution ---
def main():
    # Example investment scenarios to showcase the analyzer's capabilities
    example_scenarios = [
        "AAPL, MSFT, GOOGL",  # Tech Giants
        "NVDA, AMD, INTC",  # Semiconductor Leaders
        "TSLA, F, GM",  # Automotive Innovation
        "JPM, BAC, GS",  # Banking Sector
        "AMZN, WMT, TGT",  # Retail Competition
        "PFE, JNJ, MRNA",  # Healthcare Focus
        "XOM, CVX, BP",  # Energy Sector
    ]

    # Get companies from user with example suggestion
    print("🧪 Testing Investment Report Generator with Upsonic Framework")
    print("=" * 70)
    print("\nExample scenarios:")
    for i, scenario in enumerate(example_scenarios, 1):
        print(f"{i}. {scenario}")
    
    try:
        companies = input("\nEnter company symbols (comma-separated) or press Enter for random selection: ").strip()
    except EOFError:
        # Handle non-interactive environment
        companies = ""
    
    if not companies:
        companies = random.choice(example_scenarios)
        print(f"✨ Randomly selected: {companies}")

    # Initialize workflow
    workflow = InvestmentAnalysisWorkflow()
    
    # Run complete analysis
    result = workflow.run_complete_analysis(
        companies=companies,
        message="Generate comprehensive investment analysis and portfolio allocation recommendations"
    )
    
    print("\n" + "="*70)
    print(result)


if __name__ == "__main__":
    main()
