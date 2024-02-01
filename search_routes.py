#search_routes.py
from flask import Blueprint,jsonify,request
from meilisearch import Client
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import meilisearch
from bson import ObjectId

load_dotenv()

search_bp = Blueprint('search', __name__)

meilisearch_url = os.getenv('MEILISEARCH_URL')
mongo_uri= os.getenv('MONGO_URI')

#connection to MongoDB
client = MongoClient(mongo_uri)
db = client['tmdbdb']
collection_name = db['movies']

#Connection to Meilisearch
meilisearch_client = meilisearch.Client(meilisearch_url)
# client = Client(meilisearch_url)

#Add indexes
meilisearch_index_name = 'movies'
meilisearch_index = meilisearch_client.index(meilisearch_index_name)

#create index
if meilisearch_index_name not in meilisearch_client.get_indexes():
    meilisearch_client.create_index(uid=meilisearch_index_name)


def synchronize_data():
   
    mongo_data = list(collection_name.find())

    for doc in mongo_data:
        if '_id' in doc and isinstance(doc['_id'], ObjectId):
            doc['_id'] = str(doc['_id'])


    
    meilisearch_index.add_documents(mongo_data)


@search_bp.route('/sync_data', methods=['GET'])
def sync_data():
    try:
        synchronize_data()
        return jsonify({'message': 'Data synchronization successful'})
    except Exception as e:
        return jsonify({'error': str(e)})


@search_bp.route('/search',methods=['GET'])
def search():
    query = request.args.get('query')

    try:
        search_results = meilisearch_index.search(query).get('hits', [])

        return jsonify(search_results)


    except Exception as e:
        return jsonify({'error':str(e)})



if __name__ == '__main__':
    synchronize_data()

