"""
main.py
====================
The single entry point of the project. From the project root:

    python main.py                  # API only  (http://127.0.0.1:8000/docs)
    python main.py --dashboard      # API + Streamlit dashboard together

What it does, in order:
  1. sets up logging
  2. creates the FastAPI app and registers the global exception handler
  3. on startup, starts the agent once (this also starts the MCP server and
     loads the embedding model once, instead of on every question)
  4. on shutdown, stops the agent and the MCP server cleanly

"""

import argparse
import subprocess
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.agents.agent import init_agent, shutdown_agent
from src.services.report_scheduler import start_scheduler, stop_scheduler
from src.config import constants
from src.exceptions import AppError, register_exception_handlers
from src.repositories.data_access import load_reviews
from src.routers import chat_router, dashboard_router, health_router
from src.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app):
    logger.info("Starting %s", constants.API_TITLE)

    
    try:
        load_reviews()
    except AppError as error:
        logger.error("Review data not loaded: %s", error.message)

    
    try:
        await init_agent()
    except AppError as error:
        logger.error("Agent not started: %s", error.message)

    start_scheduler()  

    yield

    logger.info("Shutting down")
    await stop_scheduler()
    await shutdown_agent()


def create_app():
    app = FastAPI(title=constants.API_TITLE, lifespan=lifespan)
    register_exception_handlers(app)
    app.include_router(health_router.router)
    app.include_router(chat_router.router)
    app.include_router(dashboard_router.router)
    return app


app = create_app()


def start_dashboard():
    """Starts the Streamlit dashboard as a child process."""
    command = [
        sys.executable, "-m", "streamlit", "run", str(constants.DASHBOARD_APP_PATH),
        "--server.port", str(constants.DASHBOARD_PORT),
    ]
    logger.info("Starting dashboard on port %s", constants.DASHBOARD_PORT)
    return subprocess.Popen(command, cwd=str(constants.PROJECT_ROOT))


def parse_args():
    parser = argparse.ArgumentParser(description="FMCG Review Intelligence")
    parser.add_argument("--dashboard", action="store_true",
                        help="also start the Streamlit dashboard")
    parser.add_argument("--host", default=constants.API_HOST)
    parser.add_argument("--port", type=int, default=constants.API_PORT)
    return parser.parse_args()


def main():
    args = parse_args()
    dashboard_process = start_dashboard() if args.dashboard else None
    try:
        uvicorn.run(app, host=args.host, port=args.port)
    finally:
        if dashboard_process is not None:
            logger.info("Stopping dashboard")
            dashboard_process.terminate()


if __name__ == "__main__":
    main()
