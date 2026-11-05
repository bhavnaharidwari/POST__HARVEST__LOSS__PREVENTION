import sqlite3
from pathlib import Path

# Database Path
DB_PATH = Path("database") / "prediction_history.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            prediction_time TEXT,

            produce_name TEXT,

            category TEXT,

            prediction TEXT,

            confidence REAL,

            risk_level TEXT

        )
    """)

    conn.commit()
    conn.close()