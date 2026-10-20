import psycopg2
from config import config 

#connection = psycopg2.connect(host = "localhost",port = "5432",database = "master",user = "postgres",password = "Pilot@123")
#we avoid this method as during deployment the code will be changed everytime so following other method 

def connect():
    connection = None
    try:
        params = config()
        print("Connecting to the postgresql database ....")
        connection = psycopg2.connect(**params)
        crsr = connection.cursor()
        print("Postgresql database version: ")
        crsr.execute("select version()")
        db_version = crsr.fetchone()
        print(db_version)
        crsr.close()
    except(Exception,psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print("Database connection terminated.")
if __name__ == "__main__":
    connect()

