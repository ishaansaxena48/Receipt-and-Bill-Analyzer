import sqlite3

conn = sqlite3.connect('receipts.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor TEXT,
    date TEXT,
    amount REAL,
    currency TEXT
)
''')
conn.commit()

def insert_receipt(data):
    cursor.execute("INSERT INTO receipts (vendor, date, amount, currency) VALUES (?, ?, ?, ?)",
                   (data['vendor'], data['date'], data['amount'], data['currency']))
    conn.commit()

def fetch_all():
    cursor.execute("SELECT * FROM receipts")
    return cursor.fetchall()
