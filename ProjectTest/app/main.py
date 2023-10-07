"""
APP instance creation.
Module to be run by uvicorn on app runtime.
"""
import logging

from app import create_app
from app.core.config import settings
from app.database.database import init_database

logging.basicConfig(
    filename=settings.LOGS_FILENAME,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: [%(filename)s] %(name)s: %(message)s",
)

app = create_app()


@app.on_event("startup")
async def startup_event() -> None:
    """App start up handling."""
    logging.info("Application start up.")
    await init_database()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """App shut down handling."""
    logging.info("Application shutdown.")


@app.get("/")
async def health_check():
    """Check APP is alive."""
    return {"status": "OK"}
