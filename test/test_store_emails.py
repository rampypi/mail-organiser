import unittest
import sqlite3
from mail.store_emails import create_table, store_emails, DB_FILE
import os

class TestStoreEmails(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up the test environment before running the tests."""
        # Create the database and table
        create_table()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        try:
            os.remove(DB_FILE)
        except FileNotFoundError:
            pass
    
    def setUp(self):
        """Set up a fresh database for each test."""
        self.conn = sqlite3.connect(DB_FILE)
        self.c = self.conn.cursor()
        self.c.execute('DELETE FROM emails')
        self.conn.commit()
    
    def tearDown(self):
        """Clean up the database after each test."""
        self.c.execute('DELETE FROM emails')
        self.conn.commit()
        self.conn.close()

    def test_create_table(self):
        """Test that the table is created correctly."""
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("PRAGMA table_info(emails)")
        columns = [row[1] for row in c.fetchall()]
        conn.close()
        expected_columns = ['id', 'snippet', 'subject', 'received_date', 'sender', 'date']
        self.assertTrue(all(col in columns for col in expected_columns))

    def test_store_emails(self):
        """Test that emails are stored correctly."""
        email_data = [
            {
                'id': '1',
                'snippet': 'Test snippet',
                'subject': 'Test subject',
                'received_date': '2024-08-04',
                'sender': 'test@example.com',
                'date': '2024-08-04'
            }
        ]
        store_emails(email_data)
        
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM emails")
        rows = c.fetchall()
        conn.close()
        
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ('1', 'Test snippet', 'Test subject', '2024-08-04', 'test@example.com', '2024-08-04'))

if __name__ == '__main__':
    unittest.main()
