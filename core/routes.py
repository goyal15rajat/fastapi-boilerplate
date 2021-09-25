from fastapi import APIRouter
from .controller import version

api_router = APIRouter()

api_router.include_router(version.router, prefix="/_version", tags=['version'])
