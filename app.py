# app.py
from config import app
from movie_routes import movies_bp
from series_routes import series_bp
from episode_routes import episodes_bp
from search_routes import search_bp

flask_app = app.app

flask_app.register_blueprint(movies_bp, url_prefix='/movies')
flask_app.register_blueprint(series_bp, url_prefix='/series')
flask_app.register_blueprint(episodes_bp,url_prefix='/episodes')
flask_app.register_blueprint(search_bp)

@flask_app.route('/')
def index():
    return "Welcome to the TMDB API!"

if __name__ == '__main__':
    flask_app.run(debug=True)