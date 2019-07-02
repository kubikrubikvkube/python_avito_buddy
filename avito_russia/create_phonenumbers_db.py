import csv
import logging
import urllib
from collections import namedtuple
from typing import Set
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


if __name__ == '__main__':
    with psycopg2.connect(dbname=POSTGRES_DBNAME, user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                          host=POSTGRES_HOST) as conn:
        logging.info("PostgreSQLSavingPipeline DB connection opened")
        client = pymongo.MongoClient()
        avito_db = client["avito"]
        detailed_collection = avito_db["detailed"]
        logging.info(f"MongoDB connection info: {client.server_info()}")
        with open('phone_numbers.csv', mode='w+', encoding='utf-8') as phonenumbers_file:
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
                            postfix = None
                            address = None
                            phone_number = None
                            Row = namedtuple('Row', 'name postfix address phone_number')
                            try:
                                name = str.strip(item['seller']['name'])
                                postfix = str.strip(item['seller']['postfix'])
                                address = str.strip(item['address'])
                                raw_phone = item['contacts']['list'][0]['value']['uri']
                                r = urllib.parse.unquote_plus(raw_phone)
                                q2 = parse_qsl(urlparse(r).query)
                                phone_number = str.strip(q2[0][1])
                            except KeyError as ke:
                                pass
                            row = Row(name, postfix, address, phone_number)
                            print(row)
                            phonenumber_writer.writerow([name, postfix, address, phone_number])

        client.close()
