import os
import requests


TMDB_API_KEY = os.getenv("TMDB_API_KEY")  # À définir dans un fichier .env ou ta config


def get_movie_data(title: str):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "fr-FR"
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
            "poster_url": f"https://image.tmdb.org/t/p/w500{result['poster_path']}" if result.get("poster_path") else None,
            "id": result["id"],
            "raw_title": title
        }
    
    return {"title": title, "release_date": None, "poster_url": None, "id": None}

def get_movie_details(movie_id: int):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "credits",
        "language": "fr-FR"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()

    # Réalisateur (dans crew)
    director = next(
        (person for person in data["credits"]["crew"] if person["job"] == "Director"),
        None
    )

    # Acteurs principaux (top 3)
    top_actors = data["credits"]["cast"][:3]

    return {
        "title": data["title"],
        "year": data["release_date"].split("-")[0] if data.get("release_date") else None,
        "poster_url": f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get("poster_path") else None,
        "director": {
            "name": director["name"],
            "picture_url": f"https://image.tmdb.org/t/p/w185{director['profile_path']}" if director and director.get("profile_path") else "/static/default-profile.png"
        } if director else None,
        "actors": [
            {
                "name": actor["name"],
                "picture_url": f"https://image.tmdb.org/t/p/w185{actor['profile_path']}" if actor.get("profile_path") else "/static/default-profile.png"
            }
            for actor in top_actors
        ],
        "overview": data["overview"],
        "id": data["id"]
    }
