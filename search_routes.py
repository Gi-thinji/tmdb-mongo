#search_routes.py
from flask import Blueprint,jsonify,request
from meilisearch import Client
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import meilisearch
from bson import ObjectId,json_util
import json

load_dotenv()

search_bp = Blueprint('search', __name__)

meilisearch_url = os.getenv('MEILISEARCH_URL')
mongo_uri= os.getenv('MONGO_URI')
master_key = os.getenv('MEILISEARCH_MASTER_KEY')

# meilisearch_client.set_master_key('your_master_key')

#connection to MongoDB
client = MongoClient(mongo_uri)
db = client['tmdbdb']
collection_name = db['movies']

#Connection to Meilisearch
meilisearch_client = meilisearch.Client(meilisearch_url,'HyjS1O06i3hU8oqen5toI90yJnKeqUXAGDmhu1AVQG0')
# client = Client(meilisearch_url)
# meilisearch_client.set_master_key('your_master_key')
#Add indexes
meilisearch_index_name = 'movies'
meilisearch_index = meilisearch_client.index(meilisearch_index_name)

#create index
if meilisearch_index_name not in meilisearch_client.get_indexes():
    meilisearch_client.create_index(uid=meilisearch_index_name)

movie_record = {

  "adult": False,
  "backdrop_path": "/kXfqcdQKsToO0OUXHcrrNCHDBzO.jpg",
  "id": 278,
  "original_language": "en",
  "original_title": "The Shawshank Redemption",
  "overview": "Framed in the 1940s for the double murder of his wife and her lover, upstanding banker Andy Dufresne begins a new life at the Shawshank prison, where he puts his accounting skills to work for an amoral warden. During his long stretch in prison, Dufresne comes to be admired by the other inmates -- including an older prisoner named Red -- for his integrity and unquenchable sense of hope.",
  "popularity": 128.87,
  "poster_path": "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
  "release_date": "1994-09-23",
  "title": "The Shawshank Redemption",
  "video": False,
  "vote_average": 8.711,
  "vote_count": 25444
}

def synchronize_data():
   
    mongo_data = list(collection_name.find())
    # print(mongo_data)

    for doc in mongo_data:
        if '_id' in doc and isinstance(doc['_id'], ObjectId):
            doc['_id'] = str(doc['_id'])
    
    print(mongo_data)

    # mongo_json= json.dumps(movie_record,default=json_util.default)
    # print(mongo_json)
    
    meilisearch_index.add_documents(mongo_data)
    documents_results = meilisearch_index.get_documents()
    print(documents_results)


    

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

