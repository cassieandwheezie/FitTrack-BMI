
import psycopg2
from db import connect_db


def view_data(search_name=""):
    connection = None

    try:
        connection = connect_db()
        search_name = search_name.strip()

        with connection.cursor() as crsr:
            query = """
                SELECT name, age, gender, height, weight,
                       bmi, category, water_intake, created_at
                FROM bmi_records
            """

            if search_name:
                query += " WHERE name ILIKE %s"
                crsr.execute(
                    query + " ORDER BY created_at DESC",
                    (f"%{search_name}%",),
                )
            else:
                crsr.execute(query + " ORDER BY created_at DESC")

            return crsr.fetchall()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Could not retrieve BMI history:", error)
        return []

    finally:
        if connection is not None:
            connection.close()
