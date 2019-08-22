import logging
from typing import Dict
from settings import MONGO_DATABASE_NAME,MONGO_USER,MONGO_PASSWORD,MONGO_HOST,MONGO_PORT
import pymongo
from pymongo.results import InsertOneResult


class MongoDB:
    def __init__(self, collection_name: str) -> None:
        connection_string = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DATABASE_NAME}"
        self.client = client = pymongo.MongoClient(host=connection_string,port=MONGO_PORT)
        print(f"MongoDB client is {client}")
        self.db = db = client[MONGO_DATABASE_NAME]
        print(f"MongoDB db is: {db}")
        self.collection = db[collection_name]
        print(f"MongoDB collection is {self.collection}")
        logging.info(f"MongoDB server info: {client.server_info()}")
        logging.info(f"MongoDB db names: {client.list_database_names()}")
        logging.info("MongoDB db_connection opened")

    def insert_one(self, json: Dict) -> InsertOneResult:
        """
        Inserts one JSON document into desired collection
        :rtype: InsertOneResult
        :param json: document
        :return: Result of Insert
        """
        return self.collection.insert_one(json)

    def close(self) -> None:
        """
        Closes MongoDB connection
        """
        self.client.close()
        logging.info(f"MongoDB connection is closed")
