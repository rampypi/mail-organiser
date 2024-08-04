import sqlite3
from authenticate_gmail import authenticate_gmail, fetch_emails

DB_FILE = 'emails.db'

def create_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS emails
                 (id TEXT PRIMARY KEY, snippet TEXT)''')
    conn.commit()
    conn.close()
    print("Table created successfully")

def store_emails(email_data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for email in email_data:
        c.execute('INSERT OR REPLACE INTO emails (id, snippet) VALUES (?, ?)', (email['id'], email['snippet']))
    conn.commit()
    conn.close()
    print("Emails stored successfully")

if __name__ == '__main__':
    create_table()
    service = authenticate_gmail()
    emails = fetch_emails(service)
    print(emails)
    store_emails(emails)
