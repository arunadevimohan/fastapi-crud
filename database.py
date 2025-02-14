from dotenv import load_dotenv
import os
from pymongo import MongoClient


load_dotenv()

mongo_uri   = os.getenv('MONGO_URI')
db_name     = os.getenv('DB_NAME')

BOOKS_COLLECTION = "books"


client = MongoClient(mongo_uri)
db     = client[db_name]

books_collection = db[BOOKS_COLLECTION]