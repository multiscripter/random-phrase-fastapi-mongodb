from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import controller

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.router.redirect_slashes = False
app.include_router(
    controller.router,
    prefix='/phrases'
)


@app.get('/', response_class=HTMLResponse)
async def root():
    with open('index.html') as f:
        return f.read()
