# 💰 AI Investment Report Generator - Professional Edition

A sophisticated, production-ready investment analysis system built with modern software architecture, featuring FastAPI backend, Streamlit UI, and AI-powered analysis using the **Upsonic AI Agent Framework**.

## 🚀 Features

### 🎯 **Three-Stage Analysis Workflow**
1. **Comprehensive Stock Analysis** - Market research and financial metrics evaluation
2. **Investment Potential Ranking** - Comparative analysis and risk-reward assessment  
3. **Strategic Portfolio Allocation** - Optimized allocation recommendations

### 🤖 **AI-Powered Agents**
- **Stock Analyst**: Elite market analysis and financial evaluation specialist
- **Research Analyst**: Investment ranking and comparative analysis expert
- **Investment Lead**: Portfolio strategy and allocation optimization professional

### 🏗️ **Modern Architecture**
- **FastAPI Backend**: RESTful API with async processing and automatic documentation
- **Streamlit UI**: Interactive, user-friendly web interface
- **Pydantic Models**: Type-safe data validation and serialization
- **Structured Logging**: Comprehensive logging with rotation and error tracking
- **Configuration Management**: Environment-based settings with validation

### 📊 **Professional Outputs**
- Interactive web dashboard
- RESTful API endpoints
- Professional markdown reports
- Structured JSON data for integration
- Real-time analysis tracking

## 🛠️ Installation & Setup

### 1. **Clone and Setup**
```bash
git clone <your-repo>
cd ai-investment-report-generator
git checkout project  # Use the enhanced version
```

### 2. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Configuration**
Set your API key as an environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
# or
export ANTHROPIC_API_KEY="your-api-key-here"
```

## 🚀 Quick Start

### **Option 1: Development Mode (Recommended)**
Starts both API and UI automatically:
```bash
python run_dev.py
```

### **Option 2: Individual Services**

**Start FastAPI Backend:**
```bash
python run_api.py
```

**Start Streamlit UI** (in another terminal):
```bash
python run_ui.py
```

### **Option 3: Legacy CLI Mode**
```bash
python investment_report_generator.py
```

## 🌐 Access Points

Once running, access the application through:

- **🎨 Streamlit UI**: http://localhost:8501
- **📡 FastAPI Backend**: http://localhost:8000
- **📚 API Documentation**: http://localhost:8000/docs
- **🔍 ReDoc Documentation**: http://localhost:8000/redoc

## 💼 Usage Examples

### **Web Interface (Recommended)**
1. Open http://localhost:8501 in your browser
2. Enter company symbols (e.g., "AAPL, MSFT, GOOGL")
3. Click "Start Analysis"
4. View results in interactive dashboard

### **API Usage**
```bash
# Create analysis
curl -X POST "http://localhost:8000/analyses" \
     -H "Content-Type: application/json" \
     -d '{"companies": ["AAPL", "MSFT", "GOOGL"]}'

# Get analysis result
curl "http://localhost:8000/analyses/{request_id}"

# List all analyses
curl "http://localhost:8000/analyses"
```

### **Pre-configured Example Scenarios**
1. **Tech Giants**: `AAPL, MSFT, GOOGL`
2. **Semiconductor Leaders**: `NVDA, AMD, INTC`
3. **Automotive Innovation**: `TSLA, F, GM`
4. **Banking Sector**: `JPM, BAC, GS`
5. **Retail Competition**: `AMZN, WMT, TGT`
6. **Healthcare Focus**: `PFE, JNJ, MRNA`
7. **Energy Sector**: `XOM, CVX, BP`

## 📁 Project Structure

```
ai-investment-report-generator/
├── src/
│   ├── api/              # FastAPI backend
│   │   ├── main.py       # API application
│   │   └── dependencies.py
│   ├── core/             # Core business logic
│   │   ├── agents.py     # AI agent definitions
│   │   ├── analyzer.py   # Analysis workflow
│   │   ├── exceptions.py # Custom exceptions
│   │   └── logging_config.py
│   ├── models/           # Data models
│   │   └── schemas.py    # Pydantic models
│   ├── services/         # Service layer
│   │   └── investment_service.py
│   ├── ui/               # Streamlit UI
│   │   └── streamlit_app.py
│   └── config/           # Configuration
│       └── settings.py   # Settings management
├── reports/              # Generated reports
├── logs/                 # Application logs
├── run_api.py           # API server launcher
├── run_ui.py            # UI launcher
├── run_dev.py           # Development launcher
└── requirements.txt     # Dependencies
```

## 📊 Analysis Output

The system generates comprehensive reports through multiple channels:

### **📈 Stock Analysis**
- Market position and financial metrics
- Performance analysis and analyst recommendations
- Industry trends and competitive landscape
- Risk factors and growth potential

### **🏆 Investment Ranking**
- Detailed company rankings by investment potential
- Investment rationale for each company
- Risk evaluation and mitigation strategies
- Growth potential assessment

### **💼 Portfolio Allocation**
- Specific allocation percentages
- Investment thesis and strategic rationale
- Risk management approach
- Final actionable recommendations

## ⚙️ Configuration Options

Configure the application via environment variables:

```bash
# API Configuration
export API_HOST=0.0.0.0
export API_PORT=8000
export DEBUG=true

# Model Configuration
export DEFAULT_MODEL=openai/gpt-4o-mini
export MAX_TOKENS=4000
export TEMPERATURE=0.1

# Logging
export LOG_LEVEL=INFO

# Report Management
export REPORTS_DIR=./reports
export MAX_REPORT_AGE_DAYS=30
```

## 🔧 Development Features

### **Logging & Monitoring**
- Structured logging with colored console output
- Rotating file logs with error separation
- Service statistics and health monitoring
- Real-time analysis tracking

### **Error Handling**
- Custom exception hierarchy
- Graceful degradation
- Comprehensive error reporting
- API error responses with details

### **Data Validation**
- Pydantic models for type safety
- Input validation and sanitization
- Structured response schemas
- Automatic API documentation

## 🐳 Production Deployment

### **Docker Support** (Coming Soon)
```bash
# Build and run with Docker
docker build -t investment-analyzer .
docker run -p 8000:8000 -p 8501:8501 investment-analyzer
```

### **Environment Variables for Production**
```bash
export DEBUG=false
export LOG_LEVEL=WARNING
export API_RELOAD=false
export OPENAI_API_KEY=your_production_key
```

## 📚 API Documentation

The FastAPI backend provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### **Key Endpoints**
- `POST /analyses` - Create new analysis
- `GET /analyses` - List all analyses
- `GET /analyses/{id}` - Get specific analysis
- `DELETE /analyses/{id}` - Delete analysis
- `GET /health` - Health check
- `GET /stats` - Service statistics

## 🧪 Testing

```bash
# Run API health check
curl http://localhost:8000/health

# Test analysis creation
curl -X POST http://localhost:8000/analyses \
     -H "Content-Type: application/json" \
     -d '{"companies": ["AAPL"]}'
```

## 🔒 Security Considerations

- Environment-based configuration
- Input validation and sanitization
- Rate limiting (planned)
- API key management
- Error message sanitization in production

## 📈 Performance Features

- Async processing for non-blocking operations
- Response caching for analysis results
- Efficient report generation and storage
- Background task processing
- Resource cleanup and management

## 🤝 Framework Integration

Built with **Upsonic AI Agent Framework** ([docs.upsonic.ai](https://docs.upsonic.ai/)):

✅ **Safety-First Design**: Built-in safety engines and validation  
✅ **Structured Outputs**: Python objects for easy integration  
✅ **Agent Teams**: Reliable multi-agent collaboration  
✅ **Production Ready**: FastAPI compatible and scalable  
✅ **Memory & Context**: Advanced memory management capabilities

## ⚠️ Disclaimer

**Important**: This tool is for educational and research purposes only. The analysis provided should not be considered as financial advice. Always consult with qualified financial advisors before making investment decisions.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🆘 Troubleshooting

### **Common Issues**

**API Key Not Found:**
```bash
export OPENAI_API_KEY=your_key_here
python run_dev.py
```

**Port Already in Use:**
```bash
export API_PORT=8001
export STREAMLIT_PORT=8502
python run_dev.py
```

**Import Errors:**
```bash
# Ensure you're in the project root directory
cd ai-investment-report-generator
python run_dev.py
```

### **Getting Help**
- Check the logs in the `logs/` directory
- View API documentation at http://localhost:8000/docs
- Open an issue on GitHub

---

Built with ❤️ using modern Python architecture and [Upsonic AI Agent Framework](https://docs.upsonic.ai/)