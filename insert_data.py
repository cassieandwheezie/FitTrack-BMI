
import psycopg2
from db import connect_db


def insert_data(name, age, gender, height, weight, bmi, category, water_intake):
    connection = None
    crsr = None

    try:
        connection = connect_db()
        crsr = connection.cursor()

        # Check whether the same record was saved
        # within the last 30 seconds.
        check_query = """
            SELECT 1
            FROM bmi_records
            WHERE LOWER(TRIM(name)) = LOWER(TRIM(%s))
              AND age = %s
              AND gender = %s
              AND height = %s
              AND weight = %s
              AND created_at >= NOW() - INTERVAL '30 seconds'
            LIMIT 1;
        """

        crsr.execute(
            check_query,
            (name, age, gender, height, weight)
        )

        if crsr.fetchone():
            connection.rollback()
            return False

        # Insert only when no recent duplicate exists
        insert_query = """
            INSERT INTO bmi_records
            (name, age, gender, height, weight, bmi,
             category, water_intake)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """

        crsr.execute(
            insert_query,
            (
                name.strip(), age, gender, height, weight,
                bmi, category, water_intake
            )
        )

        connection.commit()
        return True

    except psycopg2.DatabaseError as error:
        if connection is not None:
            connection.rollback()

        print("Database error:", error)
        return None

    finally:
        if crsr is not None:
            crsr.close()

        if connection is not None:
            connection.close()
