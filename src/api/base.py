from fastapi import APIRouter

from .url import router as router_url

# from .user import router as router_user

api_router = APIRouter()
# api_router.include_router(router_user)
api_router.include_router(router_url)

