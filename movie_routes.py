from flask import Blueprint,jsonify
from config import TMDB_API_KEY,mongo
import requests

TMDB_API_URL = 'https://api.themoviedb.org/3/'

movies_bp = Blueprint('movies_bp',__name__)

@movies_bp.route('/movies')
def fetch_movies():
    try:
        endpoint = 'movie/top_rated'
        params = {'api_key': TMDB_API_KEY}
        response = requests.get(f'{TMDB_API_URL}{endpoint}', params=params)
        response.raise_for_status

        movies = response.json()['results']

        save_to_db(movies)

        return jsonify({'message': 'Movies fetched and saved successfully'})
    except requests.RequestException as e:
        return jsonify({'success': False, 'message': f'Error fetching movies: {str(e)}'})


    # mongo.db.tv_series.insert_many(movies)

    # return movies

def save_to_db(movies):
    try:
        mongo.db.movies.delete_many({})

        mongo.db.movies.insert_many(movies)
    except Exception as e:
        
        return jsonify({ 'message': f'Error saving movies to MongoDB: {str(e)}'})



