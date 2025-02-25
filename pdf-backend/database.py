import sqlite3
from flask import g

# Function to get the database connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("pdf_data.db")
        g.db.row_factory = sqlite3.Row  # Enable row access by name
    return g.db

# Function to get the database cursor
def get_cursor():
    if 'cursor' not in g:
        g.cursor = get_db().cursor()
    return g.cursor

# Initialize the database (create tables if they don't exist)
def init_db():
    db = get_db()
    cursor = get_cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pdf_text (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            extracted_text TEXT NOT NULL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()

# Save extracted text to the database
def save_to_db(filename, extracted_text):
    db = get_db()
    cursor = get_cursor()
    cursor.execute('''
        INSERT INTO pdf_text (filename, extracted_text)
        VALUES (?, ?)
    ''', (filename, extracted_text))
    db.commit()

# Fetch all stored data
def get_all_data():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM pdf_text")
    rows = cursor.fetchall()
    return rows

# Fetch data for a specific file
def get_single_data(id):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM pdf_text WHERE id = ?", (id,))
    row = cursor.fetchone()
    return row

# Close the database connection
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()