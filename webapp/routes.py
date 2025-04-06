from fastapi import APIRouter

from .controllers import index

ui_router = APIRouter()
ui_router.include_router(index.router, prefix="/index", tags=["index"])
