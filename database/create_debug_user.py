import sqlite3
import bcrypt

username = "debug"
password = "debug"

password_hash = bcrypt.hashpw(
    password.encode('utf-8'),
    bcrypt.gensalt()
)

conn = sqlite3.connect("table_top_aid.db")
cursor = conn.cursor()

cursor.execute(
    """
    INSERT INTO users (username, password_hash)
    VALUES (?, ?)
    """,
    (
        username,
        password_hash.decode('utf-8')
    )
)

conn.commit()
conn.close()

print("Debug user successfully created")
