
import psycopg2
import bcrypt
from db import connect_db


def register_user(email, password):
    connection = None

    try:
        email = email.strip().lower()

        if not email or len(password) < 8:
            return False, "Enter an email and a password of at least 8 characters."

        connection = connect_db()

        with connection.cursor() as crsr:
            crsr.execute(
                """
                INSERT INTO users (email, password_hash)
                VALUES (%s, %s)
                RETURNING user_id;
                """,
                (
                    email,
                    bcrypt.hashpw(
                        password.encode("utf-8"),
                        bcrypt.gensalt()
                    ).decode("utf-8")
                )
            )

            user_id = crsr.fetchone()[0]

        connection.commit()
        return True, user_id

    except psycopg2.IntegrityError:
        if connection:
            connection.rollback()
        return False, "This email is already registered."

    except Exception as error:
        if connection:
            connection.rollback()
        print("Registration error:", error)
        return False, "Registration failed. Please try again."

    finally:
        if connection:
            connection.close()


def login_user(email, password):
    connection = None

    try:
        email = email.strip().lower()
        connection = connect_db()

        with connection.cursor() as crsr:
            crsr.execute(
                """
                SELECT user_id, password_hash
                FROM users
                WHERE email = %s;
                """,
                (email,)
            )
            user = crsr.fetchone()

        if user and bcrypt.checkpw(
            password.encode("utf-8"),
            user[1].encode("utf-8")
        ):
            return True, user[0]

        return False, "Invalid email or password."

    except Exception as error:
        print("Login error:", error)
        return False, "Login failed. Please try again."

    finally:
        if connection:
            connection.close()
