import sqlite3
from mail.authenticate_gmail import authenticate_gmail, fetch_emails

DB_FILE = 'emails.db'

def create_table():
    """Create the emails table in the SQLite database if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id TEXT PRIMARY KEY,
            snippet TEXT,
            subject TEXT,
            received_date TEXT,
            sender TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Table created successfully")

def store_emails(email_data):
    """Store fetched emails into the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for email in email_data:
        c.execute('''
            INSERT OR REPLACE INTO emails (id, snippet, subject, received_date, sender, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (email['id'], email['snippet'], email.get('subject', ''), email.get('received_date', ''), email.get('sender', ''), email.get('date', '')))
    conn.commit()
    conn.close()
    print("Emails stored successfully")

if __name__ == '__main__':
    create_table()
    service = authenticate_gmail()
    emails = fetch_emails(service)
    print(emails)
    store_emails(emails)
