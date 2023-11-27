from config import app
from movie_routes import movies_bp
from series_routes import series_bp

app.register_blueprint(movies_bp, url_prefix='/movies')
app.register_blueprint(series_bp, url_prefix='/series')

if __name__ == '__main__':
    app.run(debug=True)