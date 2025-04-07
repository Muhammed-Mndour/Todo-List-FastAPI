from fastapi import FastAPI

from .views.routers import router

app = FastAPI()
app.include_router(router)
