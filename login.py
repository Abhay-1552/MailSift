import psycopg2
from urllib.parse import urlparse
from psycopg2 import extensions
from psycopg2 import sql
from dotenv import load_dotenv
import os


class AnimeDB:
    def __init__(self):
        self.env = os.getenv('URL')
        self.url = urlparse(self.env)

        # Connect to the CockroachDB database using the URL
        self.conn = psycopg2.connect(
            database=self.url.path[1:],
            user=self.url.username,
            password=self.url.password,
            host=self.url.hostname,
            port=self.url.port
        )

        try:
            if self.conn.status == extensions.STATUS_READY:
                print("Connection Successful!")

        except Exception as e:
            print("Connection Failed:", e)

    def close_connection(self):
        if hasattr(self, 'conn') and self.conn is not None:
            self.conn.close()
            print("Connection Closed")


if __name__ == '__main__':
    AnimeDB()
