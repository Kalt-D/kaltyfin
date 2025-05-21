import os
import requests

TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # À définir dans un fichier .env ou ta config


def get_movie_data(title: str):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "en-GB"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    if data.get("results"):
        result = data["results"][0]
        return {
            "title": result["title"],
            "release_date": result["release_date"].split("-")[0],
            "poster_url": f"https://image.tmdb.org/t/p/w500{result['poster_path']}" if result.get("poster_path") else None
        }
    
    return {"title": title, "release_date": None, "poster_url": None}