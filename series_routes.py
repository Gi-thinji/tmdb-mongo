#series_routes.py
from flask import Blueprint,jsonify
from config import tmdb_api_key,app
import requests
from logger_config import logger_config

logger = logger_config()

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
        logger.info('TV series fetched and saved successfully')
        return jsonify({'message': 'TV series fetched and saved successfully'})
        
    except requests.RequestException as e :
        logger.error(f'Error fetching TV Series: {str(e)}')
        return jsonify({'success': False, 'message': f'Error fetching TV Series: {str(e)}'}),500


def save_to_db(tv_show):
    try:
        mongo.db.tv_series.delete_many({})

        mongo.db.tv_series.insert_one(tv_show)
        logger.info("TV Series saved to MongoDB successfully")
    except Exception as e:
        logger.error(f'Error saving TV series to MongoDB: {str(e)}')
        return jsonify({ 'message': f'Error saving TV series to MongoDB: {str(e)}'}),500