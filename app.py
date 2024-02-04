# app.py
from config import app
from movie_routes import movies_bp
from series_routes import series_bp
from episode_routes import episodes_bp
from search_routes import search_bp
import logging
from logging.handlers import TimedRotatingFileHandler
import os

flask_app = app.app

# log_dir = '/var/log/cast'
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)

# log_file = os.path.join(log_dir, 'app.log')
# handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=7)
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# app.logger.addHandler(handler)

flask_app.register_blueprint(movies_bp, url_prefix='/movies')
flask_app.register_blueprint(series_bp, url_prefix='/series')
flask_app.register_blueprint(episodes_bp,url_prefix='/episodes')
flask_app.register_blueprint(search_bp)



@flask_app.route('/')
def index():
    return "Welcome to the TMDB API!"

if __name__ == '__main__':
    flask_app.run(debug=True)