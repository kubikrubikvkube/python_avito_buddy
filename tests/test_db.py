import sqlite3
import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        conn = sqlite3.connect('example.db')
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS avito_simple_ads
                     (id integer,
                     category text,
                     location text,
                     coords text,
                     time integer,
                     title text,
                     usertype text,
                     images text,
                     services text,
                     price text,
                     uri text,
                     uri_mweb text,
                     isVerified text,
                     isFavorite text)''')

        # Insert a row of data
        c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()


if __name__ == '__main__':
    unittest.main()
