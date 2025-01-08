from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .flower import flower

app = FastAPI()


@app.get("/api/{pad_to}")
def web(pad_to: int = 42):
    return flower(pad_to)

app.mount("/", StaticFiles(directory="static"), name="static")
