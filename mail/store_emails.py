import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import os
from store_emails import create_table, store_emails, DB_FILE


class TestStoreEmails(unittest.TestCase):

    def setUp(self):
        """Setup a temporary database file before each test."""
        self.db_file = DB_FILE
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def tearDown(self):
        """Remove the temporary database file after each test."""
        if os.path.exists(self.db_file):
            os.remove(self.db_file)

    def test_create_table(self):
        """Test the creation of the database table."""
        create_table()
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('PRAGMA table_info(emails)')
        columns = c.fetchall()
        conn.close()
        self.assertEqual(len(columns), 2)
        self.assertEqual(columns[0][1], 'id')
        self.assertEqual(columns[1][1], 'snippet')

    @patch('sqlite3.connect')
    def test_store_emails(self, mock_connect):
        """Test storing emails in the database."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        email_data = [
            {'id': '1', 'snippet': 'Test email 1'},
            {'id': '2', 'snippet': 'Test email 2'}
        ]

        store_emails(email_data)

        # Check if execute was called with the correct SQL and data
        calls = [
            unittest.mock.call('INSERT OR REPLACE INTO emails (id, snippet) VALUES (?, ?)', ('1', 'Test email 1')),
            unittest.mock.call('INSERT OR REPLACE INTO emails (id, snippet) VALUES (?, ?)', ('2', 'Test email 2'))
        ]
        mock_conn.cursor().execute.assert_has_calls(calls)
        mock_conn.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
