from fastapi import FastAPI
from tests.dummy import read_root

app = FastAPI()


app.include_router(read_root, prefix="/")
