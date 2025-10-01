#!/usr/bin/env python3
"""Run the Streamlit UI application"""

import os
import sys
import subprocess
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.config.settings import settings

def main():
    """Main entry point for Streamlit UI"""
    
    print(f"🎨 Starting Streamlit UI...")
    print(f"🌐 UI will be available at: http://{settings.streamlit_host}:{settings.streamlit_port}")
    print(f"📡 Make sure FastAPI backend is running at: http://{settings.api_host}:{settings.api_port}")
    
    # Streamlit app path (use standalone version)
    app_path = Path(__file__).parent / "streamlit_app.py"
    
    # Run Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_path),
        "--server.address", settings.streamlit_host,
        "--server.port", str(settings.streamlit_port),
        "--theme.base", "light",
        "--theme.primaryColor", "#1f77b4",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Streamlit UI stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
