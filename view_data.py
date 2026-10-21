
import psycopg2
from db import connect_db


def view_data(user_id, search_name=""):
    connection = None

    try:
        connection = connect_db()

        if connection is None:
            return []

        search_name = search_name.strip()

        with connection.cursor() as crsr:
            query = """
                SELECT name, age, gender, height, weight,
                       bmi, category, water_intake, created_at
                FROM bmi_records
                WHERE user_id = %s
            """

            params = [user_id]

            if search_name:
                query += " AND name ILIKE %s"
                params.append(f"%{search_name}%")

            query += " ORDER BY created_at DESC"

            crsr.execute(query, tuple(params))
            return crsr.fetchall()

    except psycopg2.DatabaseError as error:
        print("Could not retrieve BMI history:", error)
        return []

    finally:
        if connection is not None:
            connection.close()
