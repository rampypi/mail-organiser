Certainly! Here is the updated README.md structure based on the provided
information:

markdown Copy code \# Mail Organiser

Mail Organiser is a Python project designed to manage and process emails
using Gmail\'s API. The project includes features for storing emails in
a SQLite database, applying rules to process them, and interacting with
Gmail.

\## Features

\- \*\*Fetch Emails:\*\* Connect to Gmail and fetch emails. - \*\*Store
Emails:\*\* Save fetched emails to a SQLite database. - \*\*Process
Emails:\*\* Apply rules to emails and perform actions based on those
rules. - \*\*Rule Application:\*\* Supports string and date-based rule
application.

\## Project Structure

mail_organiser/ │ ├── mail/ │ ├── init.py │ ├── authenticate_gmail.py │
├── process_emails.py │ └── store_emails.py │ ├── tests/ │ ├── init.py │
├── test_authenticate_gmail.py │ ├── test_process_emails.py │ └──
test_store_emails.py │ ├── .gitignore ├── README.md └── requirements.txt

markdown Copy code

\## Requirements

1\. Python 3.11+ 2. \`google-auth\` 3. \`google-auth-oauthlib\` 4.
\`google-auth-httplib2\` 5. \`google-api-python-client\` 6. \`sqlite3\`
7. \`requests\` 8. \`unittest\`

\## Setup

\### 1. Clone the Repository

\`\`\`bash git clone https://github.com/rampypi/mail-organiser.git cd
mail-organiser 2. Create a Virtual Environment bash Copy code python -m
venv .venv source .venv/bin/activate \# On Windows use
\`.venv\\Scripts\\activate\` 3. Install Dependencies bash Copy code pip
install -r requirements.txt 4. Configure Gmail API Go to the Google
Cloud Console. Create a new project or select an existing one. Enable
the Gmail API for your project. Create OAuth 2.0 credentials and
download the credentials.json file. Save credentials.json in the mail/
directory. 5. Create the Database and Store Emails Run the following
script to create the SQLite database and store emails:

bash Copy code python mail/store_emails.py 6. Process Emails Run the
following script to process emails based on the rules defined in
rules.json:

bash Copy code python mail/process_emails.py Configuration Rules File
(rules.json) Define the rules for processing emails in the rules.json
file. An example is shown below:

json Copy code \[ { \"field\": \"Subject\", \"predicate\": \"contains\",
\"value\": \"urgent\", \"actions\": \[\"mark_as_read\"\],
\"logical_predicate\": \"Any\" }, { \"field\": \"Received\",
\"predicate\": \"less_than\", \"value\": \"30\", \"actions\":
\[\"move_message\"\], \"logical_predicate\": \"All\" } \] Tests Running
Tests To run the unit tests, use the following command:

bash Copy code python -m unittest discover -s tests
