import unittest
from unittest.mock import patch, MagicMock
import pickle

from mail.authenticate_gmail import authenticate_gmail, fetch_emails

class TestAuthenticateGmail(unittest.TestCase):

    @patch('mail.authenticate_gmail.pickle.load')
    @patch('mail.authenticate_gmail.pickle.dump')
    @patch('mail.authenticate_gmail.build')
    @patch('mail.authenticate_gmail.InstalledAppFlow.from_client_secrets_file')
    @patch('mail.authenticate_gmail.Request')
    def test_authenticate_gmail(self, MockRequest, MockFlow, MockBuild, mock_pickle_dump, mock_pickle_load):
        # Mock for InstalledAppFlow
        mock_flow = MagicMock()
        MockFlow.return_value = mock_flow
        mock_flow.run_local_server.return_value = MagicMock()

        # Mock for build
        mock_service = MagicMock()
        MockBuild.return_value = mock_service

        # Mock for token.pickle loading
        mock_pickle_load.return_value = None

        # Call the function
        service = authenticate_gmail()

        # Assertions
        MockFlow.assert_called_once_with('/Users/ramaselvam/repos/mail_organiser/mail/credentials.json', ['https://www.googleapis.com/auth/gmail.readonly'])
        mock_flow.run_local_server.assert_called_once()
        MockBuild.assert_called_once_with('gmail', 'v1', credentials=mock_flow.run_local_server.return_value)
        mock_pickle_dump.assert_called_once()

    @patch('mail.authenticate_gmail.build')
    def test_fetch_emails(self, MockBuild):
        # Mock service and API responses
        mock_service = MagicMock()
        MockBuild.return_value = mock_service

        # Mock response for list() and get()
        mock_service.users().messages().list.return_value.execute.return_value = {'messages': [{'id': '12345'}]}
        mock_service.users().messages().get.return_value.execute.return_value = {
            'id': '12345',
            'snippet': 'Test snippet',
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'test@example.com'},
                    {'name': 'Subject', 'value': 'Test Subject'},
                    {'name': 'Date', 'value': 'Thu, 01 Aug 2024 12:00:00 +0000'}
                ]
            }
        }

        email_data = fetch_emails(mock_service)

        # Assertions
        self.assertEqual(len(email_data), 1)
        self.assertEqual(email_data[0]['id'], '12345')
        self.assertEqual(email_data[0]['snippet'], 'Test snippet')
        self.assertEqual(email_data[0]['from'], 'test@example.com')
        self.assertEqual(email_data[0]['subject'], 'Test Subject')
        self.assertEqual(email_data[0]['date'], 'Thu, 01 Aug 2024 12:00:00 +0000')

if __name__ == '__main__':
    unittest.main()
