from __future__ import absolute_import

import csv
import logging
import sqlite3
import urllib
from typing import Optional
from urllib.parse import urlparse, parse_qsl

from console_progressbar import ProgressBar
from mongodb import MongoDB
from postgres import PostgreSQL
from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DBNAME

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler("phonenumbers.log"),
        logging.StreamHandler()
    ])



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

def strip(string_to_strip: str) -> str:
    return str.strip(string_to_strip)

if __name__ == '__main__':
    names_db = NamesDatabase()
    pgsql = PostgreSQL(POSTGRES_DBNAME, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST)
    mongo = MongoDB("detailed")
    with open('phone_numbers.csv', mode='w', newline='', encoding='utf-8') as phonenumbers_file:
        items = pgsql.select_items(POSTGRES_DBNAME, is_detailed=True)
        print("\n")
        pb = ProgressBar(total=len(items), prefix='Generating CSV file...', decimals=2, length=50, fill='X', zfill='-')
        pb_x = 0
        for id in items:
            pb_x += 1
            pb.print_progress_bar(pb_x)
            item = mongo.collection.find_one(id)
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
                writer = csv.writer(phonenumbers_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([name, gender, postfix, address, phone_number])
