from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.recipes.router import router as recipes_router
from app.users.router import router as users_router

api_router = APIRouter()
api_router.include_router(auth_router, tags=['auth'])
api_router.include_router(recipes_router, prefix='/recipes', tags=['recipes'])
api_router.include_router(users_router, prefix='/users', tags=['users'])
