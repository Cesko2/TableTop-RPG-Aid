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

def insert_sheet(user_id, sheet_type, save_data):
    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO sheets (user_id, type, data)
            VALUES (?, ?, ?)
            """,
            (user_id, sheet_type, save_data)
        )

        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()

def update_sheet(user_id, sheet_id, sheet_type, save_data):
    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE sheets
            SET type = ?, data = ?
            WHERE id = ? AND user_id = ?
            """,
            (sheet_type, save_data, sheet_id, user_id)
        )

        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()

def get_sheets_from_database(user_id):
    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                type,
                data
            FROM sheets
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        )
    
        return cursor.fetchall()
    finally:
        connection.close()

def get_sheet_from_database(user_id, sheet_id):
    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                type,
                data
            FROM sheets
            WHERE id = ?
                AND user_id = ?
            """,
            (sheet_id, user_id)
        )

        return cursor.fetchone()
    finally:
        connection.close()
