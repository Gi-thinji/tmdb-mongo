from config import app
from movie_routes import movies_bp

app.register_blueprint(movies_bp, url_prefix='/movies')






if __name__ == '__main__':
    app.run(debug=True)