import os
import re

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services import get_movie_data

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def clean_title(filename):
    name = os.path.splitext(filename)[0]
    name = name.replace(".", " ").replace("_", " ")
    name = re.sub(r'(19\d{2}|20\d{2})', '', name)
    name = re.sub(r'(1080p|720p|bluray|x264|h264|webrip|webdl|dvdrip)', '', name, flags=re.IGNORECASE)
    return name.strip()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    video_dir = "media/Films"
    video_files = [
        f for f in os.listdir(video_dir)
        if f.lower().endswith((".mp4", ".mkv", ".avi"))
    ]
    medias = []
    for file in video_files:
        raw_title = clean_title(file)
        movie_data = get_movie_data(raw_title)
        medias.append({
            "title": movie_data["title"],
            "year": movie_data["release_date"],
            "poster_url": movie_data["poster_url"]
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "medias": medias
    })

