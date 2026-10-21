
import psycopg2
from db import connect_db


def insert_data(
    user_id, name, age, gender, height, weight,
    bmi, category, water_intake
):
    connection = None

    try:
        connection = connect_db()

        if connection is None:
            return None

        with connection.cursor() as crsr:
            crsr.execute(
                """
                INSERT INTO bmi_records (
                    user_id, name, age, gender, height,
                    weight, bmi, category, water_intake
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    user_id, name.strip(), age, gender,
                    height, weight, bmi, category, water_intake
                )
            )

        connection.commit()
        return True

    except psycopg2.DatabaseError as error:
        if connection is not None:
            connection.rollback()

        print("Could not save BMI record:", error)
        return None

    finally:
        if connection is not None:
            connection.close()
