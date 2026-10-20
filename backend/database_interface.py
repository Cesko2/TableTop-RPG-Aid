import sqlite3
from pathlib import Path

DATABASE_PATH = (Path(__file__).resolve().parent.parent / "database" / "table_top_aid.db")

def get_database_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def get_user_by_username(username):
    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                user_id,
                username,
                password_hash
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        row = cursor.fetchone()
        if row is None:
            return None

        return dict(row)
    finally:
        connection.close()

def insert_user(username, password_hash):
    #TODO:Define this function later
    pass
