from prettytable import PrettyTable
from personal_helper.console.colorizer import Colorizer
from personal_helper.console.file_operations import read_contacts, write_contacts
from personal_helper.console.command_logger import read_commands_log


# Define all command functions
def command_help():
    commands_description = [
        ("help", "help", "Display a list of available commands with details."),
        ("hello", "hello", "Greet and interact with the bot."),
        ("close or exit", "close or exit", "Terminate the bot session."),
        ("add-contact", "add-contact [name] [phone]",
         "Create a new contact or add an additional phone number to an existing one."),
        ("all-contacts", "all-contacts", "List all contacts in the Address Book."),
        ("change-contact", "change-contact [name] [field] [old_value] [new_value]",
         "Modify contact details like phone, email, name, or birthday."),
        ("find-contact", "find-contact [name]", "View specific details of a contact."),
        ("delete-contact", "delete-contact [name]", "Remove a specific contact from the Address Book."),
        ("show-phone", "show-phone [name]", "Display a contact’s phone numbers."),
        ("add-birthday", "add-birthday [name] [birthday_date]", "Include a birthday for a contact."),
        ("show-birthday", "show-birthday [name]", "Show the birthday of a specific contact."),
        ("birthdays", "birthdays [quantity_of_days]", "List upcoming birthdays within a specified number of days."),
        ("add-email", "add-email [name] [email]", "Add an email address for a contact."),
        ("show-email", "show-email [name]", "Display the email addresses of a specific contact."),
        ("change-email", "change-email [name] [old_email] [new_email]", "Update a contact’s email address."),
        ("delete-email", "delete-email [name] [email]", "Remove a specific email address from a contact."),
        ("add-address", "add-address [name] [address]", "Assign an address to a contact."),
        ("show-address", "show-address [name]", "View the address associated with a contact."),
        ("delete-address", "delete-address [name]", "Delete the address of a contact."),
        ("add-note", "add-note [title] [content] [tags]", "Create a new note with title, content, and optional tags."),
        ("delete-note", "delete-note [title]", "Remove a note by its title."),
        ("change-note", "change-note [title] [new_content] [new_tags]", "Edit the content and/or tags of a note."),
        ("find-note-by-title", "find-note-by-title [title]", "Locate a note by its title."),
        ("find-note-by-tag", "find-note-by-tag [tag]", "Search for notes by a specific tag."),
        ("show-all-notes", "show-all-notes", "Display all notes in the system."),
        ("show-commands", "show-commands", "List all commands entered so far.")
    ]

    table = PrettyTable()
    table.field_names = ["Command", "Usage", "Description"]
    for command in commands_description:
        table.add_row(command)
    print(Colorizer.info(table))


def command_hello():
    print(Colorizer.success("Hello! How can I assist you today?"))


def command_exit():
    print(Colorizer.success("Exiting the command interpreter. Goodbye!"))
    exit()


def command_add_contact(name, phone):
    contacts = read_contacts()
    if name in contacts:
        contacts[name]['phones'].append(phone)
    else:
        contacts[name] = {'phones': [phone]}
    write_contacts(contacts)
    print(Colorizer.success(f"Contact {name} added/updated successfully."))


def command_all_contacts():
    contacts = read_contacts()
    if not contacts:
        print(Colorizer.info("No contacts found."))
        return

    table = PrettyTable()
    table.field_names = ["Name", "Phones"]
    for name, info in contacts.items():
        table.add_row([name, ", ".join(info['phones'])])
    print(Colorizer.info(table))


def command_change_contact(name, field, old_value, new_value):
    contacts = read_contacts()
    if name not in contacts:
        print(Colorizer.error(f"Contact {name} not found."))
        return

    if field == 'phone':
        if old_value in contacts[name]['phones']:
            contacts[name]['phones'].remove(old_value)
            contacts[name]['phones'].append(new_value)
            write_contacts(contacts)
            print(Colorizer.success(f"Contact {name}'s phone changed successfully."))
        else:
            print(Colorizer.error(f"Old phone number {old_value} not found for contact {name}."))
    else:
        print(Colorizer.error(f"Field {field} not supported."))


def command_find_contact(name):
    contacts = read_contacts()
    if name not in contacts:
        print(Colorizer.error(f"Contact {name} not found."))
        return

    table = PrettyTable()
    table.field_names = ["Name", "Phones"]
    table.add_row([name, ", ".join(contacts[name]['phones'])])
    print(Colorizer.info(table))


def command_delete_contact(name):
    contacts = read_contacts()
    if name in contacts:
        del contacts[name]
        write_contacts(contacts)
        print(Colorizer.success(f"Contact {name} deleted successfully."))
    else:
        print(Colorizer.error(f"Contact {name} not found."))


def command_show_phone(name):
    contacts = read_contacts()
    if name not in contacts:
        print(Colorizer.error(f"Contact {name} not found."))
        return

    table = PrettyTable()
    table.field_names = ["Name", "Phones"]
    table.add_row([name, ", ".join(contacts[name]['phones'])])
    print(Colorizer.info(table))


def command_add_birthday(name, birthday_date):
    contacts = read_contacts()
    if name in contacts:
        contacts[name]['birthday'] = birthday_date
        write_contacts(contacts)
        print(Colorizer.success(f"Birthday for contact {name} added successfully."))
    else:
        print(Colorizer.error(f"Contact {name} not found."))


def command_show_birthday(name):
    contacts = read_contacts()
    if name not in contacts or 'birthday' not in contacts[name]:
        print(Colorizer.error(f"Birthday for contact {name} not found."))
        return

    table = PrettyTable()
    table.field_names = ["Name", "Birthday"]
    table.add_row([name, contacts[name]['birthday']])
    print(Colorizer.info(table))


def command_birthdays(quantity_of_days):
    print(Colorizer.info(f"Showing birthdays within {quantity_of_days} days"))


def command_add_email(name, email):
    contacts = read_contacts()
    if name in contacts:
        if 'emails' not in contacts[name]:
            contacts[name]['emails'] = []
        contacts[name]['emails'].append(email)
        write_contacts(contacts)
        print(Colorizer.success(f"Email for contact {name} added successfully."))
    else:
        print(Colorizer.error(f"Contact {name} not found."))


def command_show_email(name):
    contacts = read_contacts()
    if name not in contacts or 'emails' not in contacts[name]:
        print(Colorizer.error(f"Emails for contact {name} not found."))
        return

    table = PrettyTable()
    table.field_names = ["Name", "Emails"]
    table.add_row([name, ", ".join(contacts[name]['emails'])])
    print(Colorizer.info(table))


def command_change_email(name, old_email, new_email):
    contacts = read_contacts()
    if name not in contacts or 'emails' not in contacts[name]:
        print(Colorizer.error(f"Emails for contact {name} not found."))
        return

    if old_email in contacts[name]['emails']:
        contacts[name]['emails'].remove(old_email)
        contacts[name]['emails'].append(new_email)
        write_contacts(contacts)
        print(Colorizer.success(f"Email for contact {name} changed successfully."))
    else:
        print(Colorizer.error(f"Old email {old_email} not found for contact {name}."))


def command_delete_email(name, email):
    contacts = read_contacts()
    if name not in contacts or 'emails' not in contacts[name]:
        print(Colorizer.error(f"Emails for contact {name} not found."))
        return

    if email in contacts[name]['emails']:
        contacts[name]['emails'].remove(email)
        write_contacts(contacts)
        print(Colorizer.success(f"Email for contact {name} deleted successfully."))
    else:
        print(Colorizer.error(f"Email {email} not found for contact {name}."))


def command_add_address(name, address):
    contacts = read_contacts()
    if name in contacts:
        contacts[name]['address'] = address
        write_contacts(contacts)
        print(Colorizer.success(f"Address for contact {name} added successfully."))
    else:
        print(Colorizer.error(f"Contact {name} not found."))


def command_show_address(name):
    contacts = read_contacts()
    if name not in contacts or 'address' not in contacts[name]:
        print(Colorizer.error(f"Address for contact {name} not found."))
        return

    table = PrettyTable()
    table.field_names = ["Name", "Address"]
    table.add_row([name, contacts[name]['address']])
    print(Colorizer.info(table))


def command_delete_address(name):
    contacts = read_contacts()
    if name in contacts and 'address' in contacts[name]:
        del contacts[name]['address']
        write_contacts(contacts)
        print(Colorizer.success(f"Address for contact {name} deleted successfully."))
    else:
        print(Colorizer.error(f"Address for contact {name} not found."))


def command_add_note(title, content, tags):
    print(Colorizer.info(f"Adding note with title: {title}, content: {content}, tags: {tags}"))


def command_delete_note(title):
    print(Colorizer.info(f"Deleting note with title: {title}"))


def command_change_note(title, new_content, new_tags):
    print(Colorizer.info(f"Changing note with title: {title}, new content: {new_content}, new tags: {new_tags}"))


def command_find_note_by_title(title):
    print(Colorizer.info(f"Finding note with title: {title}"))


def command_find_note_by_tag(tag):
    print(Colorizer.info(f"Finding notes with tag: {tag}"))


def command_show_all_notes():
    print(Colorizer.info("Showing all notes"))


def command_show_commands():
    commands_log = read_commands_log()
    if not commands_log:
        print(Colorizer.info("No commands found."))
        return

    table = PrettyTable()
    table.field_names = ["Command"]
    for command in commands_log:
        table.add_row([command.strip()])
    print(Colorizer.info(table))


def display_command_menu():
    """
    Display the command menu at the start of the application.
    """
    print(Colorizer.highlight("Available Commands:"))
    command_help()
