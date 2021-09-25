import os

from fastapi import FastAPI

from core.routes import api_router as core_router
from core.settings import app_configs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


app = FastAPI(
    title="FastApi bolierplate",
    description="FastApi bolierplate",
    debug=app_configs.DEBUG,
    contact={
        "name": "",
        "url": "http://host.example.com/api/",
    },
    docs_url=app_configs.DOCS_URL,
    redoc_url=app_configs.REDOC_URL,
)

app.include_router(core_router, prefix="/api")
