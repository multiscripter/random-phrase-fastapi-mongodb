import os
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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
famd_app.debug = True
templates = Jinja2Templates(directory=f'{root_dir}templates')


# Used template engine Jinja2.
# https://jinja.palletsprojects.com/en/2.11.x/templates/
@famd_app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    service = controller.get_service()
    data = service.get_index_data()
    data['request'] = request
    print(data)
    return templates.TemplateResponse('index.html', data)
