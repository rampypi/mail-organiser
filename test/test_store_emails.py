import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import re
from mail.store_emails import create_table, store_emails

class TestStoreEmails(unittest.TestCase):

    @patch('mail.store_emails.sqlite3.connect')
    def test_create_table(self, mock_connect):
        # Mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Call the function
        create_table()

        # Assertions
        mock_connect.assert_called_once_with('emails.db')
        mock_conn.cursor.assert_called_once()
        
        # Define the expected SQL command as a regex pattern
        expected_pattern = r'^CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+emails\s*\(\s*id\s+TEXT\s+PRIMARY\s+KEY\s*,\s+snippet\s+TEXT\s*\)\s*$'
        
        # Get the actual SQL command from the mock
        actual_sql = mock_cursor.execute.call_args[0][0].strip()
        
        # Use regex to check if the actual SQL command matches the expected pattern
        self.assertTrue(re.match(expected_pattern, actual_sql))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('mail.store_emails.sqlite3.connect')
    def test_store_emails(self, mock_connect):
        # Mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Sample email data
        email_data = [
            {'id': '12345', 'snippet': 'Test snippet 1'},
            {'id': '67890', 'snippet': 'Test snippet 2'}
        ]

        # Call the function
        store_emails(email_data)

        # Assertions
        mock_connect.assert_called_once_with('emails.db')
        mock_conn.cursor.assert_called_once()
        # Check if the execute method was called with the correct parameters
        mock_cursor.execute.assert_any_call('INSERT OR REPLACE INTO emails (id, snippet) VALUES (?, ?)', ('12345', 'Test snippet 1'))
        mock_cursor.execute.assert_any_call('INSERT OR REPLACE INTO emails (id, snippet) VALUES (?, ?)', ('67890', 'Test snippet 2'))
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
