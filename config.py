from flask import Flask,Blueprint
from pymongo import MongoClient

app= Flask(__name__)
tmdb_bp = Blueprint('tmdb', __name__, url_prefix='/tmdb')

TMDB_API_KEY = 'bdafc4661430ae309b0b69639ed9c4ed'
MONGO_URI = 'mongodb://localhost:27017/'

DB_NAME = 'tmdb_database'
client = MongoClient(MONGO_URI)

db = client[DB_NAME]

tmdb_bp = Blueprint('tmdb', __name__, url_prefix='/tmdb')
