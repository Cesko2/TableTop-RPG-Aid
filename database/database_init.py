import sqlite3
import bcrypt
from pathlib import Path

DATABASE_PATH = "table_top_aid.db"

def get_database_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def build_sheet_table():
    connection = get_database_connection()
    connection.execute("PRAGMA foreign_keys = ON;")

    try:
        cursor = connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sheets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                data TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
            """
        )
    finally:
        connection.close()

def build_user_table():
    connection = get_database_connection()
    
    try:
        cursor = connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            );
            """
        )
    finally:
        connection.close()

def create_debug_user():
    connection = get_database_connection()
    password = "debug"
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            ("debug", password_hash)
        )
        connection.commit()
    finally:
        connection.close()

build_user_table()
build_sheet_table()
create_debug_user()
