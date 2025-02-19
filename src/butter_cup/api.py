from http import HTTPStatus
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from .flower import flower

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/api/{pad_to}",)
def web(pad_to: int = 42):
    return flower(pad_to)


# Explicitly map /favicon.ico
# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return FileResponse("static/favicon.ico")

# Or if you want to redirect
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse("/static/favicon.ico",status_code=HTTPStatus.MOVED_PERMANENTLY)