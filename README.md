# Email Processing Project

This project consists of a standalone Python script that authenticates to Google’s Gmail API using OAuth, fetches a list of emails from your Inbox, stores them in a SQLite database, and processes them based on rules defined in a JSON file. The processing is done through a REST API.

## Features

1. **Authenticate with Google’s Gmail API**: Uses OAuth for authentication.
2. **Fetch Emails**: Retrieves a list of emails from Gmail's Inbox.
3. **Store Emails**: Stores email data in an SQLite database.
4. **Process Emails**: Processes emails based on rules stored in a JSON file.
5. **Rules-Based Processing**: Defines rules with conditions and actions.

## Prerequisites

1. **Python 3.6+**
2. **Pip** (Python package installer)
3. **Google Cloud Project** with Gmail API enabled

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/username/repository.git
cd repository
```

### 2. Install Dependencies

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Configure Google API

1. **Set up Google Cloud Project**:
   - Create a project on [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the Gmail API.
   - Create OAuth 2.0 credentials (Client ID and Secret).

2. **Download OAuth Credentials**:
   - Save the JSON file with OAuth 2.0 credentials as `credentials.json` in the project directory.

### 4. Configure SQLite Database

The project uses SQLite as the database. No additional configuration is needed for SQLite beyond ensuring the `emails.db` file can be created in the project directory.

### 5. JSON Rules File

Create a JSON file named `rules.json` in the project directory. Define your rules with conditions and actions. Example format:

```json
{
    "all_rules": [
        {
            "field": "Subject",
            "predicate": "contains",
            "value": "secrets",
            "actions": ["mark_as_read"],
            "logical_predicate": "Any"
        }
    ],
    "any_rules": [
        {
            "field": "Subject",
            "predicate": "contains",
            "value": "urgent",
            "actions": ["archive"],
            "logical_predicate": "Any"
        },
        {
            "field": "From",
            "predicate": "equals",
            "value": "example@example.com",
            "actions": ["notify"],
            "logical_predicate": "Any"
        }
    ]
}


```

### 6. Run the Scripts

1. **Fetch and Store Emails**:

   ```bash
   python mail/store_emails.py
   ```

   This script will authenticate with Google’s Gmail API, fetch emails, and store them in the SQLite database `emails.db`. It also creates the `emails` table if it does not exist.

2. **Process Emails Based on Rules**:

   ```bash
   python mail/process_emails.py
   ```

   This script will read the rules from `rules.json`, process the emails stored in the database, and perform the specified actions.

## Example Usage

1. **Fetch and Store Emails**:
   ```bash
   python mail/store_emails.py
   ```

2. **Process Emails**:
   ```bash
   python mail/process_emails.py
   ```
## Runnin test cases

```bash
   python3 -m unittest discover -s test
   ```

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. Ensure your changes adhere to the existing coding style and include appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
