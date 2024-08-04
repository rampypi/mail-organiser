import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
from mail.process_emails import (
    load_rules,
    apply_string_rule,
    apply_date_rule,
    apply_rule,
    filter_emails,
    process_emails,
    apply_actions
)

class TestProcessEmails(unittest.TestCase):

    @patch('mail.process_emails.open', new_callable=unittest.mock.mock_open, read_data='{"all_rules": [], "any_rules": []}')
    def test_load_rules(self, mock_open):
        rules = load_rules()
        mock_open.assert_called_once_with('rules.json', 'r')
        self.assertEqual(rules, {"all_rules": [], "any_rules": []})

    def test_apply_string_rule(self):
        self.assertTrue(apply_string_rule('hello world', 'contains', 'world'))
        self.assertFalse(apply_string_rule('hello world', 'does_not_contain', 'world'))
        self.assertTrue(apply_string_rule('hello world', 'equals', 'hello world'))
        self.assertFalse(apply_string_rule('hello world', 'does_not_equal', 'hello world'))

    def test_apply_date_rule(self):
        now = datetime.now(timezone.utc)
        past_date = (now - timedelta(days=10)).strftime("%a, %d %b %Y %H:%M:%S %z")
        future_date = (now + timedelta(days=10)).strftime("%a, %d %b %Y %H:%M:%S %z")

        # Test less_than predicate
        self.assertTrue(apply_date_rule(past_date, 'less_than', '5'))
        self.assertFalse(apply_date_rule(future_date, 'less_than', '5'))

        # Test greater_than predicate
        self.assertFalse(apply_date_rule(past_date, 'greater_than', '5'))
        self.assertTrue(apply_date_rule(future_date, 'greater_than', '5'))

    @patch('mail.process_emails.sqlite3.connect')
    @patch('mail.process_emails.load_rules', return_value={'all_rules': [{'field': 'subject', 'predicate': 'contains', 'value': 'Test', 'actions': ['mark_as_read']}], 'any_rules': []})
    def test_process_emails(self, mock_load_rules, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mocking fetchall() to return sample email data
        mock_cursor.fetchall.return_value = [
            ('12345', 'Test snippet', 'Test Subject', 'Thu, 01 Aug 2024 12:00:00 +0000', 'test@example.com', 'Thu, 01 Aug 2024 12:00:00 +0000')
        ]

        # Mocking print
        with patch('builtins.print') as mock_print:
            with patch('mail.process_emails.apply_actions') as mock_apply_actions:
                process_emails()

                # Check database interactions
                mock_connect.assert_called_once_with('emails.db')
                mock_conn.cursor.assert_called_once()
                mock_cursor.execute.assert_called_once_with('SELECT id, snippet, subject, received_date, sender, date FROM emails')
                mock_conn.close.assert_called_once()

                # Check print outputs
                mock_print.assert_any_call("Processing email 12345")

                # Ensure apply_actions is called
                mock_apply_actions.assert_called_once_with(
                    {'id': '12345', 'snippet': 'Test snippet', 'subject': 'Test Subject', 'received_date': 'Thu, 01 Aug 2024 12:00:00 +0000', 'sender': 'test@example.com', 'date': 'Thu, 01 Aug 2024 12:00:00 +0000'},
                    ['mark_as_read']
                )

    @patch('mail.process_emails.apply_actions')
    def test_apply_actions(self, mock_apply_actions):
        email = {'id': '12345'}
        actions = ['mark_as_read', 'move_message']
        
        with patch('builtins.print') as mock_print:
            apply_actions(email, actions)
            # Check if print is called with the correct arguments
            mock_print.assert_any_call("Marking email 12345 as read")
            mock_print.assert_any_call("Moving email 12345 to a different folder")

if __name__ == '__main__':
    unittest.main()
