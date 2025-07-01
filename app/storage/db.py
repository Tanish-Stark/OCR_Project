import sqlite3
from datetime import datetime

DB_PATH = "data/db.sqlite3"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            language_detected TEXT,
            text TEXT,
            upload_time TEXT,
            num_pages INTEGER,
            doc_type TEXT,
            filepath TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_document(filename, text, language, num_pages, doc_type, filepath):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO documents (filename, language_detected, text, upload_time, num_pages, doc_type, filepath)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (filename, language, text, datetime.utcnow().isoformat(), num_pages, doc_type, filepath))
    conn.commit()
    conn.close()
