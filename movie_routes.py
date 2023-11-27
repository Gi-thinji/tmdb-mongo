from flask import Blueprint
from config import TMDB_API_KEY
import requests

movies_bp = Blueprint('movies_bp',__name__)

@movies_bp.route('/movies')
def fetch_movies():
    TMDB_API_URL = 'https://api.themoviedb.org/3/'

    endpoint = 'movie/top_rated'
    params = {'api_key': TMDB_API_KEY}
    response = requests.get(f'{TMDB_API_URL}{endpoint}', params=params)
    movies = response.json()['results']

    return movies

