"""

Personal Assistant

This is a personal assistant bot that can help you manage your contacts and notes.

Commands:
- hello: Greet and interact with the bot.
- close or exit: Terminate the bot session.
- add-contact [name] [phone]: Create a new contact or add an additional phone number to an existing one.
- all-contacts: List all contacts in the Address Book.
- change-contact [name] [field] [old_value] [new_value]: Modify contact details like phone, email, name, or birthday.
- find-contact [name]: View specific details of a contact.
- delete-contact [name]: Remove a specific contact from the Address Book.
- show-phone [name]: Display a contact’s phone numbers.
- add-birthday [name] [birthday_date]: Include a birthday for a contact.
- show-birthday [name]: Show the birthday of a specific contact.
- birthdays [quantity_of_days]: List upcoming birthdays within a specified number of days.
- add-email [name] [email]: Add an email address for a contact.
- show-email [name]: Display the email addresses of a specific contact.
- change-email [name] [old_email] [new_email]: Update a contact’s email address.
- delete-email [name] [email]: Remove a specific email address from a contact.
- add-address [name] [address]: Assign an address to a contact.
- show-address [name]: View the address associated with a contact.
- delete-address [name]: Delete the address of a contact.
- add-note [title] [content] [tags]: Create a new note with title, content, and optional tags.
- delete-note [title]: Remove a note by its title.
- change-note [title] [new_content] [new_tags]: Edit the content and/or tags of a note.
- find-note-by-title [title]: Locate a note by its title.
- find-note-by-tag [tag]: Search for notes by a specific tag.

Type 'help' to see a list of available commands.

"""

from helper import main

if __name__ == "__main__":
    main()
