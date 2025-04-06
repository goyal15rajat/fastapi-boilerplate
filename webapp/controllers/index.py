from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from core.settings import templates

router = APIRouter()


@router.get("", response_class=HTMLResponse)
async def get_index(request: Request):
    """
    Welcome page route that renders the welcome.html template
    """
    return templates.TemplateResponse("welcome.html", {"request": request, "title": "Welcome to FastAPI Boilerplate"})
