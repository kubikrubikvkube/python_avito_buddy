import logging
from typing import Dict

import pymongo
from pymongo.results import InsertOneResult


class MongoDB:

    def __init__(self, collection_name: str) -> None:
        self.client = client = pymongo.MongoClient()
        self.db = db = client["avito"]
        self.collection = db[collection_name]
        logging.info("MongoDB db_connection opened")
        logging.info(f"MongoDB server info: {client.server_info()}")

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
