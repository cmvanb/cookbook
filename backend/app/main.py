from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.db import init_db
from app.core.router import api_router

init_db()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_PREFIX}/openapi.json',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix=settings.API_PREFIX)

@app.get('/')
def root():
    return {'message': 'Welcome to FastAPI!'}

# TODO: Serve frontend application
