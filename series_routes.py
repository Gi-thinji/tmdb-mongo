#series_routes.py
from flask import Blueprint,jsonify
from config import tmdb_api_key,app
import requests

mongo = app.mongo

TMDB_API_URL = 'https://api.themoviedb.org/3/'

series_bp = Blueprint('series_bp',__name__)

@series_bp.route('/series/<int:series_id>')
def fetch_series(series_id):
    try:
        endpoint = f'tv/{series_id}'
        params = {'api_key': tmdb_api_key}
        response = requests.get(f'{TMDB_API_URL}{endpoint}', params=params)
        response.raise_for_status()

        tv_show = response.json()

        save_to_db(tv_show)

        return jsonify({'message': 'TV series fetched and saved successfully'})

    except requests.RequestException as e :
        return jsonify({'success': False, 'message': f'Error fetching movies: {str(e)}'}),500


def save_to_db(tv_show):
    try:
        mongo.db.tv_series.delete_many({})

        mongo.db.tv_series.insert_one(tv_show)
    except Exception as e:
        
        return jsonify({ 'message': f'Error saving TV series to MongoDB: {str(e)}'}),500