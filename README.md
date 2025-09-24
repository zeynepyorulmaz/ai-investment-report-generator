# 💰 AI Investment Report Generator - Upsonic Version

A sophisticated investment analysis system built with the **Upsonic AI Agent Framework** that combines market research, financial analysis, and portfolio management.

## Features

🚀 **Three-Stage Analysis Workflow:**
1. **Comprehensive Stock Analysis** - Market research and financial metrics evaluation
2. **Investment Potential Ranking** - Comparative analysis and risk-reward assessment  
3. **Strategic Portfolio Allocation** - Optimized allocation recommendations

🤖 **AI-Powered Agents:**
- **MarketMaster-X**: Elite Stock Analyst specializing in market analysis and financial evaluation
- **ValuePro-X**: Senior Research Analyst for investment ranking and comparative analysis
- **PortfolioSage-X**: Investment Lead expert in portfolio strategy and allocation optimization

📊 **Structured Outputs:**
- Professional markdown reports
- Structured data models for integration
- Comprehensive analysis documentation

## Installation

1. **Clone and setup:**
```bash
git clone <your-repo>
cd ai-investment-report-generator
git checkout simple-version
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
source venv/bin/activate
python investment_report_generator.py
```

### Example Company Portfolios

Choose from pre-configured example scenarios:

1. **Tech Giants**: `AAPL, MSFT, GOOGL`
2. **Semiconductor Leaders**: `NVDA, AMD, INTC`
3. **Automotive Innovation**: `TSLA, F, GM`
4. **Banking Sector**: `JPM, BAC, GS`
5. **Retail Competition**: `AMZN, WMT, TGT`
6. **Healthcare Focus**: `PFE, JNJ, MRNA`
7. **Energy Sector**: `XOM, CVX, BP`

Or enter your own comma-separated list of stock symbols.

## Sample Output

The system generates three comprehensive reports:

### 📈 Stock Analysis Report
- Market position and financial metrics
- Performance analysis and analyst recommendations
- Industry trends and competitive landscape
- Risk factors and growth potential

### 🏆 Investment Ranking Report  
- Detailed company rankings by investment potential
- Investment rationale for each company
- Risk evaluation and mitigation strategies
- Growth potential assessment

### 💼 Portfolio Allocation Report
- Specific allocation percentages
- Investment thesis and strategic rationale
- Risk management approach
- Final actionable recommendations

## Generated Files

Reports are saved in the `reports/investment/` directory:
- `stock_analyst_report.md` - Comprehensive market analysis
- `research_analyst_report.md` - Investment ranking and rationale
- `investment_report.md` - Portfolio allocation strategy

## Framework Benefits

Built with **Upsonic AI Agent Framework** ([docs.upsonic.ai](https://docs.upsonic.ai/get_started/introduction)):

✅ **Safety-First Design**: Built-in safety engines and validation  
✅ **Structured Outputs**: Python objects for easy integration  
✅ **Agent Teams**: Reliable multi-agent collaboration  
✅ **Production Ready**: FastAPI compatible and scalable  
✅ **Memory & Context**: Advanced memory management capabilities

## Configuration

### API Keys
You'll need to set up your preferred LLM provider. Upsonic supports:
- OpenAI
- Anthropic
- Google Gemini
- Azure OpenAI
- Local models

Set your API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
# or
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Custom Models
You can easily switch between different LLM providers by modifying the agent initialization in the code.

## Example Run

```bash
$ python investment_report_generator.py

🧪 Testing Investment Report Generator with Upsonic Framework
======================================================================

Example scenarios:
1. AAPL, MSFT, GOOGL
2. NVDA, AMD, INTC
3. TSLA, F, GM
4. JPM, BAC, GS
5. AMZN, WMT, TGT
6. PFE, JNJ, MRNA
7. XOM, CVX, BP

Enter company symbols (comma-separated) or press Enter for random selection: AAPL, MSFT, GOOGL

🚀 Starting investment analysis for companies: AAPL, MSFT, GOOGL
💼 Analysis request: Generate comprehensive investment analysis and portfolio allocation recommendations

📊 PHASE 1: COMPREHENSIVE STOCK ANALYSIS
============================================================
🔍 Analyzing market data and fundamentals...
✅ Stock analysis completed and saved to reports/investment/stock_analyst_report.md

🏆 PHASE 2: INVESTMENT POTENTIAL RANKING
============================================================
📈 Ranking companies by investment potential...
✅ Investment ranking completed and saved to reports/investment/research_analyst_report.md

💼 PHASE 3: PORTFOLIO ALLOCATION STRATEGY
============================================================
💰 Developing portfolio allocation strategy...
✅ Portfolio strategy completed and saved to reports/investment/investment_report.md

🎉 INVESTMENT ANALYSIS WORKFLOW COMPLETED!
```

## Technical Architecture

### Agent Design Pattern
- **Task-Based Processing**: Each agent receives specific Task objects
- **Structured Communication**: Agents communicate through well-defined data structures
- **Modular Design**: Easy to extend with new agents or modify existing ones

### Data Flow
1. **Input**: Company symbols and analysis requirements
2. **Processing**: Three-stage agent workflow with structured handoffs
3. **Output**: Comprehensive markdown reports and structured data

### Error Handling
- Graceful degradation for missing data
- Fallback mechanisms for API failures
- Comprehensive logging for debugging

## Disclaimer

⚠️ **Important**: This tool is for educational and research purposes only. The analysis provided should not be considered as financial advice. Always consult with qualified financial advisors before making investment decisions.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

Built with ❤️ using [Upsonic AI Agent Framework](https://docs.upsonic.ai/)