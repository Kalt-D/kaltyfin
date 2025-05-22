from app.views import router as views_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(views_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")