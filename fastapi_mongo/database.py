import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_NAME = os.environ.get('DATABASE_NAME')

class Database:
    
    def __init__(self, uri: str = DATABASE_URL, db_name: str = DATABASE_NAME):
        
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.clients_collection = self.db['clients']
        self.clients_collection.create_index([('id', 1)], unique=True)