import sqlite3
import json
from datetime import datetime, timedelta

DB_FILE = 'emails.db'
RULES_FILE = 'rules.json'


def load_rules():
    with open(RULES_FILE, 'r') as f:
        return json.load(f)


def apply_string_rule(field_value, predicate, value):
    if predicate == 'contains':
        return value in field_value
    elif predicate == 'does_not_contain':
        return value not in field_value
    elif predicate == 'equals':
        return field_value == value
    elif predicate == 'does_not_equal':
        return field_value != value
    return False


def apply_date_rule(field_value, predicate, value):
    try:
        email_date = datetime.strptime(field_value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return False

    today = datetime.utcnow()
    delta = timedelta(days=int(value))
    if predicate == 'less_than':
        return email_date < today - delta
    elif predicate == 'greater_than':
        return email_date > today - delta
    return False


def apply_rule(email, rule):
    field_value = email.get(rule['field'].lower(), '')
    if rule['field'].lower() == 'received':
        return apply_date_rule(field_value, rule['predicate'], rule['value'])
    else:
        return apply_string_rule(field_value, rule['predicate'], rule['value'])


def process_emails():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, snippet FROM emails')  # Adjusted to match the actual columns
    emails = c.fetchall()
    print("Fetched emails:", emails)  # Debugging line
    conn.close()

    rules = load_rules()

    for email in emails:
        print("Email data:", email)  # Debugging line
        email_dict = {'id': email[0], 'snippet': email[1]}

        for rule in rules:
            if rule['logical_predicate'] == 'All':
                if all(apply_rule(email_dict, r) for r in rules if r['logical_predicate'] == 'All'):
                    print(f"Processing email {email_dict['id']} based on rule {rule['name']}")
                    apply_actions(email_dict, rule['actions'])
            elif rule['logical_predicate'] == 'Any':
                if any(apply_rule(email_dict, r) for r in rules if r['logical_predicate'] == 'Any'):
                    print(f"Processing email {email_dict['id']} based on rule {rule['name']}")
                    apply_actions(email_dict, rule['actions'])


def apply_actions(email, actions):
    for action in actions:
        if action == 'mark_as_read':
            print(f"Marking email {email['id']} as read")
            # Implement the logic to mark the email as read
        elif action == 'move_message':
            print(f"Moving email {email['id']} to a different folder")
            # Implement the logic to move the email to another folder
        # Add more actions as needed


if __name__ == '__main__':
    process_emails()
