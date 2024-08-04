# Email Processing Project

This project consists of a standalone Python script that authenticates to Google’s Gmail API using OAuth, fetches a list of emails from your Inbox, stores them in a relational database, and processes them based on rules defined in a JSON file. The processing is done through a REST API.

## Features

1. **Authenticate with Google’s Gmail API**: Uses OAuth for authentication.
2. **Fetch Emails**: Retrieves a list of emails from Gmail's Inbox.
3. **Store Emails**: Stores email data in a relational database (Postgres/MySQL/SQLite3).
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

### 4. Configure Database

Edit `config.py` to set up your database connection. Update the following variables with your database details:

- `DATABASE_URL` (For Postgres/MySQL)
- `DATABASE_NAME` (For SQLite3)

For example, for SQLite3:

```python
DATABASE_URL = 'sqlite:///emails.db'
```

For Postgres:

```python
DATABASE_URL = 'postgresql://username:password@localhost/dbname'
```

### 5. JSON Rules File

Create a JSON file named `rules.json` in the project directory. Define your rules with conditions and actions. Example format:

```json
[
    {
        "conditions": {
            "subject_contains": "urgent",
            "from": "example@example.com"
        },
        "actions": [
            "archive",
            "notify"
        ]
    }
]
```

### 6. Run the Scripts

1. **Fetch and Store Emails**:

   ```bash
   python fetch_emails.py
   ```

   This script will authenticate with Google’s Gmail API, fetch emails, and store them in the configured database.

2. **Process Emails Based on Rules**:

   ```bash
   python process_emails.py
   ```

   This script will read the rules from `rules.json`, process the emails stored in the database, and perform the specified actions.

## Example Usage

1. **Fetch Emails**:
   ```bash
   python fetch_emails.py
   ```

2. **Process Emails**:
   ```bash
   python process_emails.py
   ```

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. Ensure your changes adhere to the existing coding style and include appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to adjust the details according to your specific project setup and requirements. Let me know if you need any additional sections or changes!
