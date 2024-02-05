from flask import Blueprint, jsonify
from config import tmdb_api_key, app
import requests
from logger_config import logger_config

logger = logger_config()

mongo = app.mongo

TMDB_API_URL = 'https://api.themoviedb.org/3/'

episodes_bp = Blueprint('episode_bp', __name__)

@episodes_bp.route('/<int:series_id>/episodes')
def fetch_and_save_episodes(series_id):
    try:
        series_details = fetch_tvshow_details(series_id)

        if series_details:
            all_episodes = fetch_tvshow_episodes(series_id)
            save_episodes_to_db(series_id,all_episodes)
            logger.info('Episodes fetched and saved successfully')
            return jsonify({'message': 'Episodes fetched and saved successfully'})
        logger.error('Error fetching TV show details')
        return jsonify({'success': False, 'message': 'Error fetching TV show details'}), 500


    except requests.RequestException as e:
        logger.error(f'Error fetching TV show episodes: {str(e)}')
        return jsonify({'success': False, 'message': f'Error fetching TV show episodes: {str(e)}'}),500
    
def fetch_tvshow_episodes(series_id):
    try:
        endpoint = f'tv/{series_id}'
        params = {'api_key': tmdb_api_key}
        seasons = fetch_tvshow_details(series_id).get('seasons',[])

        all_episodes = []
        for season in seasons:
            season_number = season.get('season_number')
            endpoint = f'tv/{series_id}/season/{season_number}'
            season_response = requests.get(f'{TMDB_API_URL}{endpoint}', params=params)
            season_response.raise_for_status()
            episodes = season_response.json().get('episodes', [])
            all_episodes.extend(episodes)
        
        return all_episodes
    
    except requests.RequestException as e:
        logger.error(f'Error fetching TV show episodes: {str(e)}')
        return jsonify({'success': False, 'message': f'Error fetching TV show episodes: {str(e)}'}), 500




    
def fetch_tvshow_details(series_id):
    try:
        endpoint =  f'tv/{series_id}'
        params = {'api_key': tmdb_api_key}
        response = requests.get(f'{TMDB_API_URL}{endpoint}', params=params)
        response.raise_for_status()

        series_data = response.json()
        return series_data

    except requests.RequestException as e:
        logger.error(f'Error fetching TV show details: {str(e)}')
        return jsonify({'success': False, 'message': f'Error fetching TV show details: {str(e)}'}),500
    

    
def save_episodes_to_db(series_id,all_episodes):
    try:
        for episode in all_episodes:
                episode_data = {
                    'title':episode.get('name'),
                    'description':episode.get('overview'),
                    'season_number': episode.get('season_number'),
                    'episode_number': episode.get('episode_number')

                }
                if 'episodes' not in mongo.db.list_collection_names():
                    mongo.db.create_collection('episodes')

                mongo.db.episodes.insert_one(episode_data)

    except Exception as e:
        logger.error(f'Error saving episodes to MongoDB: {str(e)}')
        return jsonify({'success': False, 'message': f'Error saving episodes to MongoDB: {str(e)}'}),500


        
        

    
