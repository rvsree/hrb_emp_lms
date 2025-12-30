"""
Main entry point for HRB Employee LMS MCP Server.

This is the consolidated main.py that starts the FastAPI application.
Run with: python -m src.app.api.main
Or: uvicorn src.app.api.main:app --host 0.0.0.0 --port 8081
"""

import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.admin.health import health_router
from src.app.api.controller.mcp_controller import mcp_router
from src.app.common.config.app_logging import setup_logging, get_logger
from src.app.common.config.config import settings


# Load environment variables
load_dotenv(os.path.join(os.getcwd(), ".env"), override=False)

# Setup logging
setup_logging()
logger = get_logger("app_main")

# Create FastAPI app
app = FastAPI(
    title="HRB Employee LMS MCP Server",
    version="1.0.0",
    description="Python-based MCP server for Leave Management System"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Routers
app.include_router(health_router)
app.include_router(mcp_router)

logger.info("HRB Employee LMS MCP Server initialized")


def main():
    """Main entry point to run the server."""
    # Configure uvicorn to use our logging setup
    # log_config=None means uvicorn won't configure its own logging
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.server_port,
        log_level=settings.log_level.lower(),
        log_config=None  # Use our custom logging configuration
    )


if __name__ == "__main__":
    main()


