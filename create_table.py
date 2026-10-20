
import psycopg2
from db import connect_db


def create_table():
    connection = None

    try:
        connection = connect_db()

        with connection.cursor() as crsr:
            crsr.execute("""
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INTEGER NOT NULL CHECK (age BETWEEN 1 AND 120),
                    gender VARCHAR(10) NOT NULL,
                    height REAL NOT NULL CHECK (height > 0),
                    weight REAL NOT NULL CHECK (weight > 0),
                    bmi REAL NOT NULL CHECK (bmi > 0),
                    category VARCHAR(20) NOT NULL,
                    water_intake INTEGER NOT NULL CHECK (water_intake >= 0),
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)

        connection.commit()
        print("BMI table is ready.")

    except (Exception, psycopg2.DatabaseError) as error:
        if connection is not None:
            connection.rollback()
        print("Could not create BMI table:", error)
        raise

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    create_table()
