import unittest
import json
import sqlite3
import os
from unittest.mock import patch, mock_open
from datetime import datetime, timedelta, timezone  # Import datetime
from mail.process_emails import load_rules, apply_string_rule, apply_date_rule, apply_rule, filter_emails, process_emails, apply_actions, DB_FILE, RULES_FILE

class TestProcessEmails(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the test environment before running the tests."""
        # Create the database and rules file
        cls.create_db_and_table()
        cls.create_rules_file()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        try:
            os.remove(DB_FILE)
            os.remove(RULES_FILE)
        except FileNotFoundError:
            pass
    
    @classmethod
    def create_db_and_table(cls):
        """Create a test database and table."""
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
    
    @classmethod
    def create_rules_file(cls):
        """Create a test rules file."""
        rules = {
            "conditions": {
                "any": [
                    {"field": "subject", "predicate": "contains", "value": "Test"}
                ],
                "all": [
                    {"field": "received_date", "predicate": "greater_than", "value": "1"}
                ]
            },
            "actions": ["mark_as_read"]
        }
        with open(RULES_FILE, 'w') as f:
            json.dump(rules, f)
    
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
    
    def test_load_rules(self):
        """Test that rules are loaded correctly from the JSON file."""
        expected_rules = {
            "conditions": {
                "any": [
                    {"field": "subject", "predicate": "contains", "value": "Test"}
                ],
                "all": [
                    {"field": "received_date", "predicate": "greater_than", "value": "1"}
                ]
            },
            "actions": ["mark_as_read"]
        }
        rules = load_rules()
        self.assertEqual(rules, expected_rules)
    
    def test_apply_string_rule(self):
        """Test the string rule application."""
        self.assertTrue(apply_string_rule('Test email', 'contains', 'Test'))
        self.assertFalse(apply_string_rule('Test email', 'does_not_contain', 'Test'))
    
    def test_apply_date_rule(self):
        """Test the date rule application."""
        future_date = (datetime.now(timezone.utc) + timedelta(days=2)).strftime("%a, %d %b %Y %H:%M:%S %z")  # Updated to use timezone-aware datetime
        self.assertFalse(apply_date_rule(future_date, 'less_than', '1'))
        self.assertTrue(apply_date_rule(future_date, 'greater_than', '1'))
    
    def test_apply_rule(self):
        """Test rule application to an email."""
        email = {
            'id': '1',
            'snippet': 'Test snippet',
            'subject': 'Test subject',
            'received_date': (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%a, %d %b %Y %H:%M:%S %z"),  # Updated to use timezone-aware datetime
            'sender': 'test@example.com',
            'date': datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")
        }
        rule = {"field": "subject", "predicate": "contains", "value": "Test"}
        self.assertTrue(apply_rule(email, rule))
    
    def test_filter_emails(self):
        """Test filtering of emails based on rules."""
        email_data = [
            ('1', 'Test snippet', 'Test subject', (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%a, %d %b %Y %H:%M:%S %z"), 'test@example.com', datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z"))
        ]
        expected_result = [
            {
                'id': '1',
                'snippet': 'Test snippet',
                'subject': 'Test subject',
                'received_date': (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%a, %d %b %Y %H:%M:%S %z"),
                'sender': 'test@example.com',
                'date': datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z")
            }
        ]
        rules = {
            "conditions": {
                "any": [
                    {"field": "subject", "predicate": "contains", "value": "Test"}
                ],
                "all": [
                    {"field": "received_date", "predicate": "greater_than", "value": "1"}
                ]
            },
            "actions": ["mark_as_read"]
        }
        filtered_emails = filter_emails(email_data, rules)
        self.assertEqual(filtered_emails, expected_result)
    
    @patch('mail.process_emails.apply_actions')
    def test_process_emails(self, mock_apply_actions):
        """Test the email processing logic."""
        email_data = [
            ('1', 'Test snippet', 'Test subject', (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%a, %d %b %Y %H:%M:%S %z"), 'test@example.com', datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S %z"))
        ]
        self.c.executemany('INSERT INTO emails VALUES (?, ?, ?, ?, ?, ?)', email_data)
        self.conn.commit()

        mock_apply_actions.return_value = None
        process_emails()
        mock_apply_actions.assert_called_once()

if __name__ == '__main__':
    unittest.main()
