import psycopg2
from config import config

def connect_db():
    try:
        params = config()
        connection = psycopg2.connect(**params)
        return connection

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None