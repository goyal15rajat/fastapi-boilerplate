from fastapi import APIRouter

from .controller import external_request, version

api_router = APIRouter()

api_router.include_router(version.router, prefix="/_version", tags=['version'])
api_router.include_router(external_request.router, prefix="/external_request", tags=['external_request'])
