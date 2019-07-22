from __future__ import absolute_import

import csv
import logging
import sqlite3
from typing import Optional


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

        clean_name = name.strip().split()[0].capitalize()
        cursor = self.conn.execute("""SELECT gender FROM names WHERE name LIKE ? LIMIT 1""", [clean_name])
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def __del__(self):
        self.conn.close()
