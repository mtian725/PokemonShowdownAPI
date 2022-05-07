
from pymongo import MongoClient
from os import environ as env
from dotenv import load_dotenv, find_dotenv
import certifi
import concurrent.futures

load_dotenv(find_dotenv("config.env"))
CONNECTION_STRING = env['ATLAS_URI']
client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())

dbName = client[env['DB_NAME']]

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    for col in dbName.list_collection_names():
        executor.submit(dbName.drop_collection, col)
    
    executor.shutdown(wait=True)
