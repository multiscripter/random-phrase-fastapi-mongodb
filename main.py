import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import controller

app = FastAPI()
root_dir = __file__.split(__name__+'.py')
static_dir = root_dir[0] + 'static'
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.router.redirect_slashes = False
app.include_router(
    controller.router,
    prefix='/phrases'
)


@app.get('/', response_class=HTMLResponse)
async def root():
    with open('index.html') as f:
        return f.read()
