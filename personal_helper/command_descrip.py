from prettytable import PrettyTable
from colorizer import Colorizer


def command_help():
    commands_description = [
        ("help", "help", "Display a list of available commands with details."),
        ("hello", "hello", "Greet and interact with the bot."),        
        ("cancel or exit", "close or exit", "Terminate the bot session."),
        
        ("add-contact", "add-contact [name] [phone] [phone2] [birthday] [email] [address]",
            "Create a new contact or add an additional phone number to an existing one."),
        ("add_birthday", "add-birthday [name] [birthday_date]", "Include a birthday for a contact."),
        ("add_email", "add-email [name] [email]", "Add an email address for a contact."),
        ("add_address", "add-address [name] [address]", "Assign an address to a contact."),
        ("add_note", "add-note [title] [content] [tags]", 
            "Create a new note with title, content, and optional tags."),
        
        ("change_name", "change-name [name] | [new_value]", "Modify contact name"),
        ("change_phone", "change_phone", "Modify contact's phone"),
        ("change_birthday", "change_birthday", "Modify contact's birthday"),
        ("change_email", "change-email [name] [old_email] [new_email]", 
            "Update a contact’s email address."),
        ("change_address", "change_address", "Modify contact's address"),
        ("change_note", "change-note [title] [new_content] [new_tags]", 
            "Edit the content and/or tags of a note."),
        
        ("del_phone", "del_phone [name] [phone]", "Remove phone from a contact."),
        ("del_email", "delete-email [name] [email]", "Remove a specific email address from a contact."),
        ("del_birthday", "del_birthday [name] [birthday]", "Remove birthday from a contact."),
        ("del_address", "del-address [name]", "Delete the address of a contact."),
        ("del_note", "delete-note [title]", "Remove a note by its title."),
        ("del_contact", "del-contact [name]", "Remove a specific contact from the Address Book."),        
        
        ("show_all_contacts", "show_all", "List all contacts in the Address Book."),
        ("show_phone", "show-phone [name]", "Display a contact’s phone numbers."),
        ("show_birthday", "show-birthday [name]", "Show the birthday of a specific contact."),
        ("show_email", "show-email [name]", "Display the email addresses of a specific contact."),
        ("show_upcoming_birthdays", "birthdays [quantity_of_days]", "List upcoming birthdays within a specified number of days."),
        ("show_address", "show-address [name]", "View the address associated with a contact."),
        ("show_all-notes", "show-all-notes", "Display all notes in the system."),
                    
        ("find_contact", "find-contact [name]", "View specific details of a contact."),
        ("find_note_by_title", "find-note-by-title [title]", "Locate a note by its title."),
        ("find_note_by_tag", "find-note-by-tag [tag]", "Search for notes by a specific tag."),                
    ]

    table = PrettyTable()
    table.field_names = ["Command", "Usage", "Description"]
    for command in commands_description:
        table.add_row(command)
    print(Colorizer.info(table))