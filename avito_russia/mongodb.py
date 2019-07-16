import logging

import pymongo


class MongoDB:

    def __init__(self, collection_name: str) -> None:
        self.client = client = pymongo.MongoClient()
        self.db = db = client["avito"]
        self.collection = collection = db[collection_name]
        logging.info("MongoDB db_connection opened")
        logging.info(f"MongoDB server info: {client.server_info()}")

    def insert_one(self, json) -> None:
        self.collection.insert_one(json)

    def close(self) -> None:
        self.client.close()
        logging.info(f"MongoDB connection is closed")
