import csv
import logging
import sqlite3
import urllib
from collections import namedtuple
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


def find_all_is_detailed_items(cursor) -> Set[int]:
    cursor.execute(f"SELECT id FROM {POSTGRES_DBNAME} WHERE is_detailed = True ORDER BY random()")
    ids = set()
    for raw_id in cursor:
        id = raw_id[0]
        ids.add(id)
    return ids


class NamesDatabase:
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
        cursor = self.conn.execute("""SELECT gender FROM names WHERE name LIKE ? LIMIT 1""", [name])
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return ""

    def __del__(self):
        self.conn.close()
        logging.info("SQLite3 in-memory names database closed")


if __name__ == '__main__':
    n = NamesDatabase()
    with psycopg2.connect(dbname=POSTGRES_DBNAME, user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                          host=POSTGRES_HOST) as conn:
        logging.info("PostgreSQLSavingPipeline DB connection opened")
        client = pymongo.MongoClient()
        avito_db = client["avito"]
        detailed_collection = avito_db["detailed"]
        logging.info(f"MongoDB connection info: {client.server_info()}")
        with open('phone_numbers.csv', mode='w', newline='', encoding='utf-8') as phonenumbers_file:
            phonenumber_writer = csv.writer(phonenumbers_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            with conn.cursor() as postgresql_cursor:
                ids = find_all_is_detailed_items(postgresql_cursor)
                for id in ids:
                    for item in detailed_collection.find({"_id": id}):
                        if item['adjustParams']['vertical'] == "JOB":
                            # резюме
                            pass
                        else:
                            name = None
                            gender = None
                            postfix = None
                            address = None
                            phone_number = None
                            Row = namedtuple('Row', 'name gender postfix address phone_number')
                            try:
                                name = str.strip(item['seller']['name'])
                                gender = n.resolve_gender(name)
                                postfix = str.strip(item['seller']['postfix'])
                                address = str.strip(item['address'])
                                raw_phone = item['contacts']['list'][0]['value']['uri']
                                r = urllib.parse.unquote_plus(raw_phone)
                                q2 = parse_qsl(urlparse(r).query)
                                phone_number = str.strip(q2[0][1])
                            except (KeyError, IndexError) as e:  # why indexerror? no phone supplied?
                                pass
                            row = Row(name, gender, postfix, address, phone_number)
                            print(row)
                            phonenumber_writer.writerow([name, gender, postfix, address, phone_number])

        client.close()
