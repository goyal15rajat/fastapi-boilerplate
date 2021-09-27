import os
import time

import git
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class GetVersionResponse(BaseModel):
    version: str
    deployedOn: str


@router.get("/", response_model=GetVersionResponse)
async def manage_version():
    """Api to manage version

    Response -
    {
        "version": "v0.0.0",
        "deployedOn": "Sun Sep 26 02:31:43 2021"
    }
    """

    try:
        repo = git.Repo(search_parent_directories=True)
        version = repo.git.describe('--tags')
    except Exception:
        version = "v0.0.0"

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    creation_time = time.ctime(os.path.getmtime(base_dir))

    response = {'version': version, 'deployedOn': creation_time}
    return response
