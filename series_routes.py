from flask import Blueprint
from config import TMDB_API_KEY
import requests

TMDB_API_URL = 'https://api.themoviedb.org/3/'

series_bp = Blueprint('series_bp',__name__)

@series_bp.route('/series')
def fetch_series():

    endpoint = 'tv/top_rated'
    params = {'api_key': TMDB_API_KEY}
    response = requests.get(f'{TMDB_API_URL}{endpoint}', params=params)
    tv_series = response.json()['results']

    return tv_series
