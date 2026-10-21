
import psycopg2
from db import connect_db


def create_table():
    connection = None

    try:
        connection = connect_db()

        with connection.cursor() as crsr:

            # Create users table
            crsr.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Create BMI table for new installations
            crsr.execute("""
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(user_id),
                    name VARCHAR(100) NOT NULL,
                    age INTEGER NOT NULL
                        CHECK (age BETWEEN 1 AND 120),
                    gender VARCHAR(10) NOT NULL,
                    height REAL NOT NULL CHECK (height > 0),
                    weight REAL NOT NULL CHECK (weight > 0),
                    bmi REAL NOT NULL CHECK (bmi > 0),
                    category VARCHAR(20) NOT NULL,
                    water_intake INTEGER NOT NULL
                        CHECK (water_intake >= 0),
                    created_at TIMESTAMP NOT NULL
                        DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Add user_id to an existing BMI table
            # without deleting its existing records
            crsr.execute("""
                ALTER TABLE bmi_records
                ADD COLUMN IF NOT EXISTS user_id INTEGER
                REFERENCES users(user_id);
            """)

        connection.commit()
        print("Users and BMI tables are ready.")

    except (Exception, psycopg2.DatabaseError) as error:
        if connection is not None:
            connection.rollback()

        print("Could not create tables:", error)
        raise

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    create_table()
