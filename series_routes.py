#series_routes.py
from flask import Blueprint,jsonify
from config import tmdb_api_key,app
import requests

mongo = app.mongo

TMDB_API_URL = 'https://api.themoviedb.org/3/'

series_bp = Blueprint('series_bp',__name__)

@series_bp.route('/series')
def fetch_series():
    try:
        endpoint = 'tv/top_rated'
        params = {'api_key': tmdb_api_key}
        response = requests.get(f'{TMDB_API_URL}{endpoint}', params=params)
        response.raise_for_status()

        tv_series = response.json()['results']

        save_to_db(tv_series)

        return jsonify({'message': 'TV series fetched and saved successfully'})

    except requests.RequestException as e :
        return jsonify({'success': False, 'message': f'Error fetching movies: {str(e)}'})


def save_to_db(tv_series):
    try:
        mongo.db.tv_series.delete_many({})

        mongo.db.tv_series.insert_many(tv_series)
    except Exception as e:
        
        return jsonify({ 'message': f'Error saving TV series to MongoDB: {str(e)}'})