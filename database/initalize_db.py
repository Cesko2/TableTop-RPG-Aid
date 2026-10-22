import sqlite3

conn = sqlite3.connect("table_top_aid.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database initialized successfully.")
