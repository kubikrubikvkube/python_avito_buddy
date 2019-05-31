import random
import string
from datetime import date

from sqlalchemy import create_engine

from avito.Database import Database


class SQLiteDatabase(Database):

    def __init__(self, db_filename=None, persist=False, echo=False):
        if persist is False:
            self._engine = create_engine('sqlite:///:memory:', echo=echo)
        else:
            if db_filename is None:
                random_string = ''.join(random.choice(string.ascii_letters) for _ in range(10))
                db_filename = f'{date.today().strftime("%d_%m_%Y")}_{random_string}'
            self._engine = create_engine(f'sqlite:///{db_filename}', echo=echo)
        super().__init__()
