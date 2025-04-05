# database/mongodb.py

from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME


class MongoDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
            cls._instance.client = MongoClient(MONGO_URI)
            cls._instance.db = cls._instance.client[MONGO_DB_NAME]
        return cls._instance

    def insert(self, collection_name, data):
        collection = self.db[collection_name]
        return collection.insert_one(data).inserted_id

    def find(self, collection_name, query):
        collection = self.db[collection_name]
        return list(collection.find(query))

    def update(self, collection_name, query, update_query):
        collection = self.db[collection_name]
        return collection.update_many(query, update_query)

    def delete(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.delete_many(query)