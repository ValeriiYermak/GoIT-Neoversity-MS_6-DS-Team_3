import json

CONTACTS_FILE = 'contacts.json'

def read_contacts():
    """
    Read contacts from the JSON file.
    """
    try:
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def write_contacts(contacts):
    """
    Write contacts to the JSON file.
    """
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)