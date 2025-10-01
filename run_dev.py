#!/usr/bin/env python3
"""Development runner - starts both API and UI"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from multiprocessing import Process

def run_api():
    """Run FastAPI in a separate process"""
    subprocess.run([sys.executable, "run_api.py"])

def run_ui():
    """Run Streamlit in a separate process"""
    # Wait a bit for API to start
    time.sleep(3)
    subprocess.run([sys.executable, "run_ui.py"])

def main():
    """Main development runner"""
    print("🚀 Starting Development Environment")
    print("=" * 50)
    print("Starting both FastAPI backend and Streamlit UI...")
    print()
    
    # Start API process
    api_process = Process(target=run_api)
    api_process.start()
    
    # Start UI process
    ui_process = Process(target=run_ui)
    ui_process.start()
    
    print("✅ Both services started!")
    print()
    print("📡 FastAPI Backend: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🎨 Streamlit UI: http://localhost:8501")
    print()
    print("Press Ctrl+C to stop both services")
    
    try:
        # Wait for processes
        api_process.join()
        ui_process.join()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        
        # Terminate processes
        if api_process.is_alive():
            api_process.terminate()
            api_process.join(timeout=5)
            if api_process.is_alive():
                api_process.kill()
        
        if ui_process.is_alive():
            ui_process.terminate()
            ui_process.join(timeout=5)
            if ui_process.is_alive():
                ui_process.kill()
        
        print("👋 All services stopped")

if __name__ == "__main__":
    main()
