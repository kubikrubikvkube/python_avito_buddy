from __future__ import absolute_import

import csv
import logging
import sqlite3
import urllib
from multiprocessing.pool import Pool
from typing import Set, Optional
from urllib.parse import urlparse, parse_qsl

import psycopg2
import pymongo

from avito_russia.settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DBNAME

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("phonenumbers.log"),
        logging.StreamHandler()
    ])


def find_all_is_detailed_items(postgresql_connection) -> Set[int]:
    """
    Resolving item status  - it is stored in PostreSQL, but is it already processed and stored in MongoDB?
    :param postgresql_connection:
    :return:
    """
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT id FROM {POSTGRES_DBNAME} WHERE is_detailed = True ORDER BY random()")
        ids = set()
        for raw_id in cursor:
            id = raw_id[0]
            ids.add(id)
        return ids


class NamesDatabase:
    """
    Russian names database
    """
    def __init__(self) -> None:
        self.conn = sqlite3.connect(':memory:')
        logging.info("SQLite3 in-memory names database initialized")
        self.conn.execute("CREATE TABLE names (name text, gender text);")
        self.conn.execute("CREATE INDEX names_idx ON names(name);")
        self.conn.execute("CREATE INDEX gender_idx ON names(gender);")
        with open("names.csv", mode="r", encoding="utf-8") as names_file:
            reader = csv.DictReader(names_file)
            for row in reader:
                values = [row['name'], row['gender']]
                self.conn.execute('''INSERT INTO names(name,gender) VALUES (?,?);''', values)
        logging.info("SQLite3 in-memory names database loaded")

    def resolve_gender(self, name: str) -> Optional[str]:
        """
        Resolving gender from name
        :param name: name
        :return: gender
        """
        cursor = self.conn.execute("""SELECT gender FROM names WHERE name LIKE ? LIMIT 1""", [name.capitalize()])
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return ""

    def __del__(self):
        self.conn.close()
        logging.info("SQLite3 in-memory names database closed")


def strip(string_to_strip: str) -> str:
    return str.strip(string_to_strip)

if __name__ == '__main__':
    names_db = NamesDatabase()
    with psycopg2.connect(dbname=POSTGRES_DBNAME, user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                          host=POSTGRES_HOST) as conn:
        logging.info("PostgreSQLSavingPipeline DB connection opened")
        client = pymongo.MongoClient()
        avito_db = client["avito"]
        detailed_collection = avito_db["detailed"]
        logging.info(f"MongoDB connection info: {client.server_info()}")
        with open('phone_numbers.csv', mode='w', newline='', encoding='utf-8') as phonenumbers_file:
            pool = Pool(processes=10)
            items = find_all_is_detailed_items(conn)
            for id in items:
                def process_id(id):
                    item = detailed_collection.find_one(id)
                    if item is None or item['adjustParams']['vertical'] == "JOB":
                        # резюме или None
                        pass
                    else:
                        name = None
                        gender = None
                        postfix = None
                        address = None
                        phone_number = None
                        # Row = namedtuple('Row', 'name gender postfix address phone_number')
                        try:
                            name = strip(item['seller']['name'])
                            gender = names_db.resolve_gender(name)
                            postfix = strip(item['seller']['postfix'])
                            address = strip(item['address'])
                            raw_phone = item['contacts']['list'][0]['value']['uri']
                            r = urllib.parse.unquote_plus(raw_phone)
                            q2 = parse_qsl(urlparse(r).query)
                            phone_number = strip(q2[0][1])
                        except (KeyError, IndexError) as e:  # why indexerror? no phone supplied?
                            pass
                        # row = Row(name, gender, postfix, address, phone_number)
                        # print(row)
                        writer = csv.writer(phonenumbers_file, delimiter=',', quotechar='"',
                                            quoting=csv.QUOTE_MINIMAL)
                        writer.writerow([name, gender, postfix, address, phone_number])

                pool.apply_async(process_id(id))


        client.close()