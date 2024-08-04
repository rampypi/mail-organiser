import sqlite3
import json
from datetime import datetime, timedelta, timezone

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
        email_date = datetime.strptime(field_value, "%a, %d %b %Y %H:%M:%S %z")  # Ensure correct format
    except ValueError:
        return False

    today = datetime.now(timezone.utc)  # Use timezone-aware datetime
    delta = timedelta(days=int(value))

    if predicate == 'less_than':
        return email_date < today - delta
    elif predicate == 'greater_than':
        return email_date > today - delta
    return False


def apply_rule(email, rule):
    field_value = email.get(rule['field'].lower(), '')
    if field_value is None:  # Check if field_value is None
        field_value = ''  # Default to empty string for non-existent fields
    
    if rule['field'].lower() == 'received':
        return apply_date_rule(field_value, rule['predicate'], rule['value'])
    else:
        return apply_string_rule(field_value, rule['predicate'], rule['value'])


def filter_emails(emails, rules):
    filtered_emails = []

    for email in emails:
        email_dict = {
            'id': email[0],
            'snippet': email[1],
            'subject': email[2],
            'received_date': email[3],
            'sender': email[4],
            'date': email[5]
        }

        # Apply rules based on logical predicates
        all_conditions_met = True
        any_condition_met = False

        for rule in rules.get('all_rules', []):
            if rule.get('logical_predicate', 'All') == 'All':
                if not apply_rule(email_dict, rule):
                    all_conditions_met = False
                    break

        for rule in rules.get('any_rules', []):
            if rule.get('logical_predicate', 'Any') == 'Any':
                if apply_rule(email_dict, rule):
                    any_condition_met = True

        if any_condition_met or all_conditions_met:
            filtered_emails.append(email_dict)

    return filtered_emails




def process_emails():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, snippet, subject, received_date, sender, date FROM emails')  # Adjusted to match the actual columns
    emails = c.fetchall()
    conn.close()

    rules = load_rules()

    # Ensure 'any_rules' exists and is a list, default to an empty list if missing
    all_rules = rules.get('all_rules', [])
    any_rules = rules.get('any_rules', [])

    filtered_emails = filter_emails(emails, {'all_rules': all_rules, 'any_rules': any_rules})

    for email in filtered_emails:
        print(f"Processing email {email['id']}")

        # Apply actions based on the rules
        for rule in all_rules + any_rules:  # Ensure both types of rules are considered
            if apply_rule(email, rule):
                apply_actions(email, rule['actions'])


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
