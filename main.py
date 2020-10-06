import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import controller

# FastAPI - это ASGI-фрэймворк. Apache2 не поддерживает ASGI.
# Вэб-серверы (и др.) с поддержвой ASGI указаны по ссылке ниже:
# https://github.com/florimondmanca/awesome-asgi

famd_app = FastAPI()
root_dir = os.path.abspath(__file__).split('main.py')[0]
static_dir = root_dir + 'static'
famd_app.mount("/static", StaticFiles(directory=static_dir), name="static")
famd_app.router.redirect_slashes = False
famd_app.include_router(
    controller.router,
    prefix='/phrases'
)


@famd_app.get('/', response_class=HTMLResponse)
async def root():
    with open(root_dir + 'index.html') as f:
        return f.read()
