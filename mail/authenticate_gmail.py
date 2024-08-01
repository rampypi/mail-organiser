from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path
import pickle

# Scopes required for Gmail API access
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# Path to your OAuth 2.0 credentials file
CREDS_FILE = 'credentials.json'


def authenticate_gmail():
    """Authenticate and return the Gmail service."""
    creds = None
    # Check if token.pickle file exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If no valid credentials, request new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def fetch_emails(service, num_emails=10):
    """Fetch a list of emails from the user's inbox."""
    results = service.users().messages().list(userId='me', maxResults=num_emails).execute()
    messages = results.get('messages', [])

    email_data = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        email_data.append({
            'id': msg['id'],
            'snippet': msg['snippet']
        })
    return email_data


if __name__ == '__main__':
    service = authenticate_gmail()
    emails = fetch_emails(service)
    print(emails)
