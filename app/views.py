import os
import re

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services import get_movie_data
from app.services import get_movie_details

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
            "poster_url": movie_data["poster_url"],
            "id": movie_data["id"],
            "filename": file
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "medias": medias
    })

@router.get("/preview/{movie_id}", response_class=HTMLResponse)
async def preview(request: Request, movie_id: int, filename: str = None):
    movie = get_movie_details(movie_id)
    if not movie:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    return templates.TemplateResponse("movie_info.html", {
        "request": request,
        "movie": movie,
        "filename": filename
    })


@router.get("/view/{movie_id}", response_class=HTMLResponse)
async def view(request: Request, movie_id: int, title: str = None):
    if not title:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": "Le nom du fichier vidéo est requis."
        }, status_code=400)

    movie = get_movie_details(movie_id)
    video_path = f"/media/Films/{title}"
    return templates.TemplateResponse("player.html", {
        "request": request,
        "movie": movie,
        "video_path": video_path,
        "title": title
    })
