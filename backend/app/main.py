import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.db import init_db
from app.core.router import router

init_db()

def configure_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

def configure_router(app):
    app.include_router(router, prefix=settings.API_PREFIX)

def configure_static_files(app):
    os.makedirs(settings.UPLOADS_PATH, exist_ok=True)
    app.mount('/uploads', StaticFiles(directory=settings.UPLOADS_PATH), name='uploads')

def create_app():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f'{settings.API_PREFIX}/openapi.json',
    )
    configure_middleware(app)
    configure_router(app)
    configure_static_files(app)

    return app

app = create_app()

# TODO: Serve frontend application
