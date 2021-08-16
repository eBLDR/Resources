"""
App factory.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers import api_router
from app.core.config import settings
from app.version import VERSION


def create_app():
    """FastAPI app instance creation.
    :return: instantiated app
    :rtype: FastAPI
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_NAME,
        version=VERSION,
        openapi_url=settings.API_V1_STR + "/openapi.json",
        docs_url=settings.API_V1_STR + "/docs",
        redoc_url=settings.API_V1_STR + "/redoc",
    )

    app.include_router(api_router)

    origins = [
        "http://localhost",  # Web commercial
        "http://localhost:9000",  # Web app
        "http://localhost:8080",  # Vue debugger development
    ]

    # Add front-end app(s) as permitted origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
