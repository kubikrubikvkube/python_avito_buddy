import logging
from typing import Dict
from typing import List

import pymongo
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult

from settings import MONGO_DATABASE_NAME, MONGO_USER, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT


class MongoDB:
    def __init__(self, collection_name: str) -> None:
        connection_string = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DATABASE_NAME}"
        self.client = client = pymongo.MongoClient(host=connection_string, port=MONGO_PORT)
        print(f"MongoDB client is {client}")
        self.db = db = client[MONGO_DATABASE_NAME]
        print(f"MongoDB db is: {db}")
        self.collection = db[collection_name]
        print(f"MongoDB collection is {self.collection}")
        logging.info(f"MongoDB server info: {client.server_info()}")
        logging.info(f"MongoDB db names: {client.list_database_names()}")
        logging.info("MongoDB db_connection opened")

    def count_unique_phoneNumbers(self, filter: Dict) -> int:
        print(f"Counting unique phone numbers for {filter}")
        unique_numbers = set()
        for ad in self.collection.find(filter=filter):
            if 'phoneNumber' in ad:
                unique_numbers.add(ad['phoneNumber'])
        return len(unique_numbers)

    def find(self, filter: Dict, only_unique_phoneNumbers: bool = True, limit=None) -> List[Dict]:
        print(
            f"Finding entries by filter {filter}  with {'unique' if only_unique_phoneNumbers else 'not unique'} phone numbers")
        if limit:
            found_results_cursor: Cursor = self.collection.find(filter, limit=limit)
        else:
            found_results_cursor: Cursor = self.collection.find(filter)

        if not only_unique_phoneNumbers:
            found_documents = list(found_results_cursor)
            found_documents_size = len(found_documents)
            print(f"Found {found_documents_size} non-unique documents")
            return found_documents
        else:
            unique_numbers = set()
            unique_ads = []
            for ad in found_results_cursor:
                ad_phoneNumber = ad['phoneNumber']
                if ad_phoneNumber not in unique_numbers:
                    unique_numbers.add(ad_phoneNumber)
                    unique_ads.append(ad)
            final_results_count = len(unique_ads)
            print(f"Found {final_results_count} unique documents")
            return unique_ads


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
