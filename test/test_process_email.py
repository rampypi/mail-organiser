import unittest
from unittest.mock import patch, MagicMock
from mail.process_emails import apply_string_rule, apply_date_rule


class TestProcessEmails(unittest.TestCase):

    @patch('mail.process_emails.apply_string_rule')
    def test_apply_string_rule(self, mock_apply_string_rule):
        # Define mock input and output
        email = {'subject': 'Test Subject'}
        rule = {'field': 'subject', 'predicate': 'contains', 'value': 'Test'}

        mock_apply_string_rule.return_value = True

        # Test the function
        result = apply_string_rule(email, rule['field'], rule['predicate'], rule['value'])

        self.assertTrue(result)
        mock_apply_string_rule.assert_called_once_with(email, rule['field'], rule['predicate'], rule['value'])

    @patch('mail.process_emails.apply_date_rule')
    def test_apply_date_rule(self, mock_apply_date_rule):
        # Define mock input and output
        email = {'received': '2024-08-01T12:00:00Z'}
        rule = {'field': 'received', 'predicate': 'less than', 'value': '2024-08-02'}

        mock_apply_date_rule.return_value = True

        # Test the function
        result = apply_date_rule(rule['field'], rule['predicate'], rule['value'])

        self.assertTrue(result)
        mock_apply_date_rule.assert_called_once_with(rule['field'], rule['predicate'], rule['value'])


if __name__ == '__main__':
    unittest.main()
