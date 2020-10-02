import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import controller

# FastAPI - это ASGI-фрэймворк. Apache2 не поддерживает ASGI.
# Вэб-серверы (и др.) с поддержвой ASGI указаны по ссылке ниже:
# https://github.com/florimondmanca/awesome-asgi

app = FastAPI()
root_dir = os.path.abspath(__file__).split('main.py')
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
