# config.py
from flask import Flask,Blueprint
# from pymongo import MongoClient
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()


tmdb_api_key = os.getenv('TMDB_API_KEY')
mongo_uri = os.getenv('MONGO_URI')



class FlaskAppWrapper:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["MONGO_URI"] = mongo_uri
        self.mongo = PyMongo(self.app)

app = FlaskAppWrapper()