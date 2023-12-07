# config.py
from flask import Flask,Blueprint
# from pymongo import MongoClient
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

# app= Flask(__name__)
# tmdb_bp = Blueprint('tmdb', __name__, url_prefix='/tmdb')

# TMDB_API_KEY = 'bdafc4661430ae309b0b69639ed9c4ed'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/tmdbdb'


# client = MongoClient('localhost', 27017)
# DB_NAME = 'tmdb_database'
# db = client[DB_NAME]

tmdb_api_key = os.getenv('TMDB_API_KEY')
mongo_uri = os.getenv('MONGO_URI')

# app.config["MONGO_URI"] = mongo_uri
# mongo = PyMongo(app)

class FlaskAppWrapper:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["MONGO_URI"] = mongo_uri
        self.mongo = PyMongo(self.app)

app = FlaskAppWrapper()