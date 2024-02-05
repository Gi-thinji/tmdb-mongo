# movie_routes.py
from flask import Blueprint,jsonify
from config import tmdb_api_key,app
import requests
# # from app import logger
# import logging
# import pytz
# import datetime
# from logging.handlers import TimedRotatingFileHandler
from logger_config import logger_config

# logger=logging.getLogger()
# logger.setLevel(logging.INFO)

# file_handler = TimedRotatingFileHandler('app.log', when='midnight', backupCount=0)

# file_handler.setLevel(logging.INFO)

# formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# file_handler.setFormatter(formatter)

# tz = pytz.timezone('Africa/Nairobi')

# file_handler.converter = lambda x: datetime.fromtimestamp(x, tz)

# logger.addHandler(file_handler)
logger=logger_config()
mongo = app.mongo

TMDB_API_URL = 'https://api.themoviedb.org/3/'

movies_bp = Blueprint('movies_bp',__name__)

@movies_bp.route('/movies')
def fetch_movies():
    try:
        endpoint = 'movie/top_rated'
        params = {'api_key': tmdb_api_key}
        response = requests.get(f'{TMDB_API_URL}{endpoint}', params=params)
        response.raise_for_status()

        movies = response.json()['results']

        save_to_db(movies)
        logger.info("Movies fetched and saved successfully")

        return jsonify({'message': 'Movies fetched and saved successfully'})
    except requests.RequestException as e:
        logger.error(f'Error fetching movies: {str(e)}')
        return jsonify({'success': False, 'message': f'Error fetching movies: {str(e)}'})


    # mongo.db.tv_series.insert_many(movies)

    # return movies

def save_to_db(movies):
    try:
        mongo.db.movies.delete_many({})

        mongo.db.movies.insert_many(movies)
        logger.info("Movies saved to MongoDB successfully")
    except Exception as e:
        logger.error(f'Error saving movies to MongoDB: {str(e)}')
        return jsonify({ 'message': f'Error saving movies to MongoDB: {str(e)}'})



