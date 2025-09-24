"""Streamlit UI for Investment Report Generator"""

import streamlit as st
import requests
import json
import time
import os
import sys
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

# Add src to Python path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import settings
try:
    from src.config.settings import settings
    API_BASE_URL = f"http://{settings.api_host}:{settings.api_port}"
except ImportError:
    # Fallback if import fails
    API_HOST = os.getenv("API_HOST", "localhost")
    API_PORT = int(os.getenv("API_PORT", "8001"))
    API_BASE_URL = f"http://{API_HOST}:{API_PORT}"

# Configure Streamlit page
st.set_page_config(
    page_title="AI Investment Report Generator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)


def check_api_connection() -> bool:
    """Check if FastAPI backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def create_analysis(companies: List[str], message: str) -> Optional[Dict[str, Any]]:
    """Create a new analysis via API"""
    try:
        payload = {
            "companies": companies,
            "message": message
        }
        response = requests.post(f"{API_BASE_URL}/analyses", json=payload, timeout=300)
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.Timeout:
        st.error("Analysis request timed out. The analysis might still be running in the background.")
        return None
    except Exception as e:
        st.error(f"Error creating analysis: {str(e)}")
        return None


def get_analysis(request_id: str) -> Optional[Dict[str, Any]]:
    """Get analysis by ID"""
    try:
        response = requests.get(f"{API_BASE_URL}/analyses/{request_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching analysis: {str(e)}")
        return None


def list_analyses() -> List[Dict[str, Any]]:
    """List all analyses"""
    try:
        response = requests.get(f"{API_BASE_URL}/analyses")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error listing analyses: {str(e)}")
        return []


def get_service_stats() -> Dict[str, Any]:
    """Get service statistics"""
    try:
        response = requests.get(f"{API_BASE_URL}/stats")
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        st.error(f"Error getting stats: {str(e)}")
        return {}


def display_analysis_result(result: Dict[str, Any]):
    """Display analysis result in a formatted way"""
    if not result:
        return
    
    st.subheader(f"📊 Analysis Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Status", result.get("status", "Unknown"))
    with col2:
        st.metric("Companies", ", ".join(result.get("companies", [])))
    with col3:
        created_at = result.get("created_at", "")
        if created_at:
            created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            st.metric("Created", created_date.strftime("%Y-%m-%d %H:%M"))
    
    # Display error if analysis failed
    if result.get("status") == "failed":
        st.error(f"Analysis failed: {result.get('error_message', 'Unknown error')}")
        return
    
    # Display analysis phases with full content
    if result.get("stock_analysis"):
        with st.expander("📈 Stock Analysis", expanded=True):
            stock_analysis = result["stock_analysis"]
            st.markdown(stock_analysis.get("market_analysis", "No data available"))
    
    if result.get("investment_ranking"):
        with st.expander("🏆 Investment Ranking", expanded=True):
            ranking = result["investment_ranking"]
            st.markdown(ranking.get("ranked_companies", "No data available"))
    
    if result.get("portfolio_allocation"):
        with st.expander("💼 Portfolio Allocation", expanded=True):
            portfolio = result["portfolio_allocation"]
            st.markdown(portfolio.get("allocation_strategy", "No data available"))


def main():
    """Main Streamlit application"""
    
    st.title("💰 AI Investment Report Generator")
    st.markdown("*Powered by AI agents for comprehensive investment analysis*")
    
    # Show current API endpoint
    st.info(f"🔗 API Endpoint: {API_BASE_URL}")
    
    # Check API connection
    if not check_api_connection():
        st.error("⚠️ Cannot connect to the FastAPI backend. Please ensure it's running.")
        st.info(f"Expected API at: {API_BASE_URL}")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Settings & Stats")
        
        # Service stats
        with st.expander("📊 Service Statistics"):
            stats = get_service_stats()
            if stats:
                st.metric("Total Analyses", stats.get("total_analyses", 0))
                st.metric("Recent Analyses (24h)", stats.get("recent_analyses", 0))
                
                status_counts = stats.get("status_counts", {})
                for status, count in status_counts.items():
                    st.metric(f"{status.title()}", count)
        
        # Recent analyses
        with st.expander("📝 Recent Analyses"):
            analyses = list_analyses()
            if analyses:
                for analysis in analyses[:5]:  # Show last 5
                    companies_str = ", ".join(analysis.get("companies", []))[:30]
                    st.write(f"**{companies_str}**")
                    st.write(f"Status: {analysis.get('status', 'Unknown')}")
                    st.write(f"ID: `{analysis.get('request_id', '')[:8]}...`")
                    st.divider()
            else:
                st.write("No analyses yet")
    
    # Auto-load latest analysis if no current analysis
    if not hasattr(st.session_state, 'current_analysis'):
        analyses = list_analyses()
        if analyses and len(analyses) > 0:
            latest_analysis = analyses[0]  # Most recent
            if latest_analysis.get("status") == "completed":
                full_result = get_analysis(latest_analysis.get('request_id'))
                if full_result:
                    st.session_state.current_analysis = full_result
                    st.success("✅ Loaded latest completed analysis")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🆕 New Analysis", "📋 Analysis History", "ℹ️ About"])
    
    with tab1:
        st.header("Create New Investment Analysis")
        
        # Example scenarios
        example_scenarios = [
            "AAPL, MSFT, GOOGL",  # Tech Giants
            "NVDA, AMD, INTC",     # Semiconductor Leaders
            "TSLA, F, GM",         # Automotive Innovation
            "JPM, BAC, GS",        # Banking Sector
            "AMZN, WMT, TGT",      # Retail Competition
            "PFE, JNJ, MRNA",      # Healthcare Focus
            "XOM, CVX, BP",        # Energy Sector
        ]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Company input
            companies_input = st.text_input(
                "Enter company symbols (comma-separated)",
                placeholder="e.g., AAPL, MSFT, GOOGL",
                help="Enter 1-10 company stock symbols separated by commas"
            )
            
            # Custom message
            custom_message = st.text_area(
                "Analysis Message (Optional)",
                value="Generate comprehensive investment analysis and portfolio allocation recommendations",
                help="Customize the analysis request message"
            )
        
        with col2:
            st.write("**Example Scenarios:**")
            for i, scenario in enumerate(example_scenarios, 1):
                if st.button(f"{i}. {scenario}", key=f"example_{i}"):
                    st.session_state.selected_companies = scenario
            
            if hasattr(st.session_state, 'selected_companies'):
                companies_input = st.session_state.selected_companies
        
        # Create analysis button
        if st.button("🚀 Start Analysis", type="primary", disabled=not companies_input):
            if companies_input:
                companies = [c.strip().upper() for c in companies_input.split(",") if c.strip()]
                
                if len(companies) == 0:
                    st.error("Please enter at least one company symbol")
                elif len(companies) > 10:
                    st.error("Maximum 10 companies allowed per analysis")
                else:
                    with st.spinner("Creating analysis... This may take a few minutes."):
                        result = create_analysis(companies, custom_message)
                        
                        if result:
                            st.success(f"✅ Analysis created! ID: {result.get('request_id', 'Unknown')}")
                            st.session_state.current_analysis = result
                            st.rerun()  # Refresh to show the new analysis
    
    with tab2:
        st.header("Analysis History")
        
        analyses = list_analyses()
        
        if not analyses:
            st.info("No analyses found. Create your first analysis in the 'New Analysis' tab!")
        else:
            # Filter controls
            col1, col2 = st.columns([1, 3])
            with col1:
                status_filter = st.selectbox(
                    "Filter by status",
                    ["All", "completed", "in_progress", "failed", "pending"]
                )
            
            # Filter analyses
            filtered_analyses = analyses
            if status_filter != "All":
                filtered_analyses = [a for a in analyses if a.get("status") == status_filter]
            
            # Display analyses
            for analysis in filtered_analyses:
                with st.expander(
                    f"📊 {', '.join(analysis.get('companies', []))} - {analysis.get('status', 'Unknown')}",
                    expanded=False
                ):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**ID:** `{analysis.get('request_id', '')[:8]}...`")
                        st.write(f"**Status:** {analysis.get('status', 'Unknown')}")
                    
                    with col2:
                        created_at = analysis.get('created_at', '')
                        if created_at:
                            created_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                            st.write(f"**Created:** {created_date.strftime('%Y-%m-%d %H:%M')}")
                    
                    with col3:
                        if st.button(f"View Details", key=f"view_{analysis.get('request_id')}"):
                            full_result = get_analysis(analysis.get('request_id'))
                            if full_result:
                                st.session_state.current_analysis = full_result
                                st.rerun()
            
            # Show current analysis details if selected
            if hasattr(st.session_state, 'current_analysis'):
                st.divider()
                display_analysis_result(st.session_state.current_analysis)
    
    # Display current analysis at the bottom of all tabs
    if hasattr(st.session_state, 'current_analysis'):
        st.divider()
        st.header("📊 Current Analysis Results")
        display_analysis_result(st.session_state.current_analysis)
    
    with tab3:
        st.header("About AI Investment Report Generator")
        
        st.markdown("""
        ### 🤖 AI-Powered Investment Analysis
        
        This application uses advanced AI agents to provide comprehensive investment analysis:
        
        **🔍 Three-Stage Analysis:**
        1. **Stock Analysis** - Market research and financial evaluation
        2. **Investment Ranking** - Comparative analysis and potential assessment
        3. **Portfolio Allocation** - Strategic allocation recommendations
        
        **🚀 Key Features:**
        - Real-time market analysis
        - Professional financial research
        - Risk assessment and management
        - Portfolio optimization
        - Detailed investment rationale
        
        **⚡ Technology Stack:**
        - **Backend:** FastAPI with async processing
        - **UI:** Streamlit for interactive analysis
        - **AI:** Upsonic agent framework
        - **Models:** GPT-4 for comprehensive analysis
        
        **⚠️ Disclaimer:**
        This tool is for educational and research purposes only. 
        The analysis provided should not be considered as financial advice. 
        Always consult with qualified financial advisors before making investment decisions.
        """)
        
        st.info("💡 **Tip:** Start with one of the example scenarios to see the system in action!")


if __name__ == "__main__":
    main()
