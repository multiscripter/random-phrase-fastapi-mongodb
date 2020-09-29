from fastapi import FastAPI

import controller

app = FastAPI()
app.router.redirect_slashes = False
app.include_router(
    controller.router,
    prefix='/phrases'
)
