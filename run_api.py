#!/usr/bin/env python3
"""Run the FastAPI backend server"""

import os
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.core.logging_config import setup_logging
from src.config.settings import settings

def main():
    """Main entry point for FastAPI server"""
    
    # Setup logging
    setup_logging()
    
    # Check for API keys
    if not settings.has_any_api_key:
        print("❌ Error: No API key found!")
        print("Please set one of the following environment variables:")
        print("  - OPENAI_API_KEY=your_openai_api_key")
        print("  - ANTHROPIC_API_KEY=your_anthropic_api_key")
        print("\nExample:")
        print("  export OPENAI_API_KEY=sk-...")
        print("  python run_api.py")
        sys.exit(1)
    
    print(f"🚀 Starting FastAPI server...")
    print(f"📡 API will be available at: http://{settings.api_host}:{settings.api_port}")
    print(f"📚 API Documentation: http://{settings.api_host}:{settings.api_port}/docs")
    print(f"🔧 Debug mode: {settings.debug}")
    
    # Import and run
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )

if __name__ == "__main__":
    main()
