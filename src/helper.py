"""
This module contains helper functions for the contact book application.

Functions:
    parse_input(user_input): Parse the user input into a command and arguments.
    main(): The main function of the contact book application.

This module imports the following modules:
    re: Regular expression operations.
    pickle: Module for pickling objects.
    os: Module for operating system related functions.
    prompt_toolkit: Module for command line interface.
    colorizer: Module for colored text output.
    validators: Module for validating input.
    contact_book: Module for contact book operations.
    birthday: Module for birthday operations.
    contact_book: Module for email operations.
    command_descrip: Module for displaying command descriptions.
    notes_manager: Module for notes manager operations.

This module defines the following classes:
    AddressBook: Class representing a collection of contacts.
    Record: Class representing a contact record.
    Birthday: Class representing a birthday for a contact.
    Email: Class representing an email for a contact.
    NotesManager: Class for managing notes.

This module also defines the following constants:
    COMMANDS: List of available commands.
    COMMAND_DESCRIPTIONS: Dictionary mapping commands to their descriptions.

This module also defines the following functions:
    parse_input(user_input): Parse the user input into a command and arguments.
    main(): The main function of the contact book application.

This module also defines the following variables:
    notes_manager: The notes manager object.
    COMMANDS: List of available commands.
    command_completer: The command completer object.

This module also defines the following constants:
    COMMANDS: List of available commands.
    command_completer: The command completer object.



"""


import re
import pickle
import os
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from colorizer import Colorizer
from validators import normalize_phone
from contact_book import AddressBook, Record
from birthday import Birthday
from contact_book import Email
from command_descrip import command_help
from notes_manager import NotesManager

notes_manager = NotesManager()

COMMANDS = [
    "help",
    "hello",
    "exit",
    "cancel",
    "add_contact",
    "add_birthday",
    "add_email",
    "add_address",
    "add_note",
    "show_all_contacts",
    "show_phone",
    "show_birthday",
    "show_email",
    "show_address",
    "show_upcoming_birthdays",
    "change_name",
    "change_phone",
    "change_birthday",
    "change_email",
    "change_address",
    "change_note",
    "del_contact",
    "del_phone",
    "del_birthday",
    "del_email",
    "del_address",
    "find_contact",
    "del_note",
    "find_note_by_title",
    "find_note_by_tag",
    "show_all_notes",
]

command_completer = WordCompleter(COMMANDS, ignore_case=True)


def parse_input(user_input):
    if not user_input:
        return None, None

    command = user_input[0].lower()
    args = user_input[1:]

    if command not in COMMANDS:
        return None, None

    return command, args


def load_data(filename="contact_book.pkl"):
    if not os.path.exists(filename):
        address_book = AddressBook()
        try:
            with open(filename, "wb") as f:
                pickle.dump(address_book, f)
                return address_book
        except Exception as e:
            print(Colorizer.error(f"Error while creating the file: {e}"))
    else:
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(Colorizer.error(f"Error while reading the file: {e}"))
            return None


def save_data(book, filename="contact_book.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def main():
    book = load_data()
    session = PromptSession(completer=command_completer)
    command_help()
    print(Colorizer.info("Welcome to the assistant bot!"))

    while True:
        user_input = (
            session.prompt(HTML("<ansicyan>Enter command: </ansicyan>")).strip().split()
        )
        command, args = parse_input(user_input)

        if command in COMMANDS:
            if command in ["close", "exit"]:
                print(Colorizer.success("Good bye!"))
                save_data(book)
                break

            elif command == "hello":  # HELLO #
                print(Colorizer.success("How can I help you?"))

            elif command == "add_contact":  # ADD #
                if len(args) < 2:
                    print(
                        Colorizer.error(
                            "Error: Input requires at least two arguments: name and phone."
                        )
                    )
                    continue

                name = args[0]
                phone = args[1]
                phone2 = None
                birthday = None
                email = None
                address = None

                # Process additional arguments
                for arg in args[2:]:
                    if re.match(r"^\d{10,13}$", arg):  # check if it's a phone number
                        if not phone2:
                            phone2 = arg  # set the second phone number
                        else:
                            print(
                                Colorizer.warning(
                                    f"Warning: Ignoring additional phone number {arg}."
                                )
                            )
                    elif re.match(
                        r"\d{2}\.\d{2}\.\d{4}$", arg
                    ):  # check if it's a birthday
                        birthday = arg
                    elif re.match(
                        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", arg
                    ):  # check if it's an email
                        email = arg
                    else:
                        # Everything else is considered address
                        if address is None:
                            address = arg
                        else:
                            address += " " + arg

                # Check if the phone number is valid
                normalized_phone = normalize_phone(phone)
                if isinstance(normalized_phone, str) and normalized_phone.startswith(
                    "Invalid"
                ):
                    print(
                        Colorizer.error(
                            f"Error: Invalid phone number '{phone}'. Expected format: 10 to 13 digits."
                        )
                    )  # Show the error message
                    continue  # Missing or invalid phone number
                contact = book.find_address(name)
                if contact:
                    if normalized_phone:
                        contact.phones.add_phone(
                            normalized_phone
                        )  # add the primary phone
                        print(
                            Colorizer.info(
                                f"Phone number {normalized_phone} added to {name}."
                            )
                        )
                    if phone2:
                        normalized_phone2 = normalize_phone(phone2)
                        if isinstance(
                            normalized_phone2, str
                        ) and not normalized_phone2.startswith("Invalid"):
                            contact.phones.add_phone(
                                normalized_phone2
                            )  # Add the secondary phone
                            print(
                                Colorizer.info(
                                    f"Phone number {normalized_phone2} added to {name}."
                                )
                            )
                        else:
                            print(
                                Colorizer.warning(
                                    f"Warning: Ignoring additional phone number {phone2}."
                                )
                            )
                    if birthday:
                        if re.match(
                            r"^\d{2}\.\d{2}\.\d{4}$", birthday
                        ):  # Check the format of the birthday
                            contact.add_birthday(birthday)  # Add the birthday
                            print(
                                Colorizer.info(f"Birthday {birthday} added to {name}.")
                            )
                        else:
                            print(
                                Colorizer.error(
                                    "Error: Invalid birthday format. Expected DD.MM.YYYY."
                                )
                            )
                    if email:
                        if re.match(
                            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email
                        ):
                            contact.add_email(email)
                            print(Colorizer.info(f"Email {email} added to {name}."))
                        else:
                            print(
                                Colorizer.error(
                                    "Error: Invalid email format. Use email@domain.com."
                                )
                            )
                        continue
                    if address:
                        contact.address = address  # Add the address if it exists
                        print(Colorizer.info(f"Address {address} added to {name}."))
                else:
                    # Create a new record if the contact doesn't exist
                    phones = [phone]
                    if phone2:
                        phones.append(
                            phone2
                        )  # Add the second phone number if it exists
                    record = Record(
                        name, phones, birthday, email, address
                    )  # Given name, phones, birthday, email, address
                    book.add_address(record)
                    print(
                        Colorizer.info(
                            f"New contact {name} added with phone number: {phone}, "
                            f"second phone number: {phone2 if phone2 else 'N/A'}, "
                            f"birthday: {birthday if birthday else 'N/A'}, "
                            f"email: {email if email else 'N/A'}, "
                            f"and address: {address if address else 'N/A'}."
                        )
                    )

            elif command == "change_name":
                # print(Colorizer.info("To change a name, provide the old name and the new name, separated by a '|' symbol."))
                # print(Colorizer.info("Example: old_name | new_name"))

                if len(args) < 2 or "|" not in " ".join(args):
                    print(Colorizer.error("Error: Provide old name and new name."))
                    continue
                full_input = " ".join(args)
                if "|" not in full_input:
                    print(Colorizer.error("Error: Provide old name and new name."))
                    continue
                old_name, new_name = full_input.split("|", 1)
                old_name = old_name.strip()
                new_name = new_name.strip()

                if old_name and new_name:
                    book.change_name(old_name, new_name)
                else:
                    print(
                        Colorizer.error("Error: Provide both old name and new name.")
                    )  # Change name

            elif command == "change_phone":  # Change phone number
                if len(args) < 3:
                    print(
                        Colorizer.error(
                            "Error: Provide name, old phone, and new phone."
                        )
                    )
                else:
                    name, old_phone, new_phone = args
                    contact = book.find_address(name)
                    if contact:
                        # Normalize the new phone number
                        normalized_new_phone = normalize_phone(new_phone)

                        if contact.phones.edit_phone(old_phone, normalized_new_phone):
                            print(
                                Colorizer.info(
                                    f"Phone number changed from {old_phone} to {normalized_new_phone} for {name}."
                                )
                            )
                        else:
                            print(
                                Colorizer.info(
                                    f"Phone number {old_phone} not found for {name}."
                                )
                            )
                    else:
                        print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "show_phone":  # Find phone number
                if not args:
                    print(Colorizer.error("Error: Provide a name."))
                else:
                    name = args[0]
                    contact = book.find_address(name)
                    if contact:
                        print(
                            Colorizer.info(
                                f"{name}'s phone numbers: {', '.join(contact.phones.value)}"
                            )
                        )
                    else:
                        print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "del_phone":  # Delete phone number from contact
                try:
                    name = args[0]
                    phone_number = args[
                        1
                    ]  # Use the second argument as the phone number
                    if not name or not phone_number:
                        print(
                            Colorizer.error(
                                "Error: Both contact name and phone number are required."
                            )
                        )
                        continue
                except IndexError:
                    print(
                        Colorizer.error(
                            "Error: Both contact name and phone number are required."
                        )
                    )
                    continue
                if book.delete_phone(name, phone_number):
                    print(
                        Colorizer.info(
                            f"Phone number '{phone_number}' deleted from contact '{name}'."
                        )
                    )
                else:
                    print(
                        Colorizer.error(
                            f"Error: Contact '{name}' or phone number '{phone_number}' not found."
                        )
                    )

            elif command == "show_all_contacts":
                if not book.data:
                    print(Colorizer.info("No contacts found."))
                else:
                    for contact in book.values():
                        print(contact)

            elif command == "del_contact":  # Delete contact
                if not args:
                    print(Colorizer.error("Error: Input the contact name to delete."))
                    continue
                name = args[0]
                if book.delete_contact(name):
                    print(Colorizer.info(f"Contact '{name}' deleted."))
                else:
                    print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "add_birthday":  # Add birthday
                if not args or len(args) < 2:
                    print(Colorizer.error("Error: Input name and birthday."))
                    continue
                name, birthday = args[0], args[1]
                contact = book.find_address(name)
                if contact:
                    # check birthday format
                    if re.match(r"\d{2}\.\d{2}\.\d{4}$", birthday):
                        Birthday.add_birthday_to_contact(contact, birthday)
                        print(Colorizer.info(f"Birthday {birthday} added to {name}."))
                    else:
                        print(
                            Colorizer.error(
                                f"Error: Invalid birthday format. Expected DD.MM.YYYY."
                            )
                        )
                else:
                    print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "show_birthday":  # Show birthday
                if not args:
                    print(Colorizer.error("Error:Input a name."))
                    continue
                name = args[0]
                contact = book.find_address(name)
                if contact:
                    print(Birthday.show_birthday_of_contact(contact))
                else:
                    print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "change_birthday":  # Change birthday
                if not args:
                    print(Colorizer.error("Error: Input a name and new birthday."))
                    continue
                name = args[0]
                if len(args) < 2:
                    print(
                        Colorizer.error(
                            "Error: You must provide a new birthday in the format DD.MM.YYYY."
                        )
                    )
                    continue
                new_birthday = args[1]

                # Validate the new birthday format
                if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", new_birthday):
                    print(
                        Colorizer.error(
                            "Error: Invalid birthday format. Expected DD.MM.YYYY."
                        )
                    )
                    continue

                contact = book.find_address(name)
                if contact:
                    contact.add_birthday(
                        new_birthday
                    )  # Replace the old birthday with the new one
                    print(
                        Colorizer.info(f"Birthday of {name} changed to {new_birthday}.")
                    )
                else:
                    print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "show_upcoming_birthdays":
                if len(args) < 1:
                    print("Error: Please specify the number of days after the command.")
                else:
                    try:
                        days_ahead = int(args[0])
                        upcoming_birthdays = Birthday.get_upcoming_birthdays(
                            book, days_ahead
                        )
                        if upcoming_birthdays:
                            print("Upcoming birthdays:")
                            for ub in upcoming_birthdays:
                                print(f'{ub["name"]} on {ub["congratulation_date"]}.')
                        else:
                            print(
                                f"There are no upcoming birthdays in the next {days_ahead} days."
                            )
                    except ValueError:
                        print("Error: Please specify a valid number of days.")

            elif command == "del_birthday":
                if not args:
                    print(Colorizer.error("Error: Input a name."))
                    continue
                name = args[0]
                contact = book.find_address(name)
                if contact:
                    if contact.birthday:
                        book.delete_birthday(name)
                        print(Colorizer.info(f"Birthday of {name} deleted."))
                    else:
                        print(
                            Colorizer.error(f"Error: No birthday to remove for {name}.")
                        )
                else:
                    print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "add_email":
                if not args or len(args) < 2:
                    print(Colorizer.error("Error: Input name and email."))
                    continue
                name, email = args[0], args[1]
                contact = book.find_address(name)
                if contact:
                    if re.match(
                        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email
                    ):
                        contact.add_email(email)
                    else:
                        print(
                            Colorizer.error(
                                "Error: Invalid email format. Use email@domain.com"
                            )
                        )

            elif command == "show_email":  # Show email
                if not args:
                    print(Colorizer.error("Error:Input a name."))
                    continue
                name = args[0]
                contact = book.find_address(name)
                if contact:
                    print(Email.find_email(contact))
                else:
                    print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "change_email":
                if not args:
                    print(Colorizer.error("Error: Input name and email."))
                    continue
                name = args[0]
                if len(args) < 2:
                    print(
                        Colorizer.error(
                            "Error: You must provide a new email. Use email@domain.com"
                        )
                    )
                    continue
                new_email = args[1]
                contact = book.find_address(name)
                if contact:
                    if re.match(
                        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", new_email
                    ):
                        contact.add_email(new_email)
                    else:
                        print(
                            Colorizer.error(
                                "Error: Invalid email format. Use email@domain.com"
                            )
                        )

            elif command == "del_email":  # Delete email
                if not args:
                    print(Colorizer.error("Error: Input name and email."))
                    continue
                name = args[0]
                contact = book.find_address(name)
                if contact:
                    if Email.remove_email(contact):
                        print(Colorizer.info(f"Email for {name} deleted."))
                    else:
                        print(Colorizer.error(f"Error: No email found for {name}"))
                else:
                    print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "add_address":
                if not args or len(args) < 2:
                    print(Colorizer.error("Error: Input name and address."))
                    continue
                name = args[0]
                address = " ".join(args[1:]).strip()
                contact = book.find_address(name)
                if contact:
                    contact.add_address(address)  # Add the address
                    print(Colorizer.info(f"Address '{address}' added to '{name}'."))
                else:
                    print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "show_address":  # Show email
                if not args:
                    print(Colorizer.error("Error:Input a name."))
                    continue
                name = args[0]
                contact = book.find_address(name)
                if contact:
                    if contact.address:
                        print(Colorizer.info(f"Address for {name}: {contact.address}"))
                    else:
                        print(
                            Colorizer.error(f"Error: Contact '{name}' has no address.")
                        )
                else:
                    print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "change_address":  # Change address
                if len(args) < 3 or "|" not in args:
                    print(
                        Colorizer.error(
                            "Error: Provide name, old address, |, and new address."
                        )
                    )
                    continue
                separator_index = args.index("|")
                name = args[0]
                old_address = " ".join(args[1:separator_index])
                new_address = " ".join(args[separator_index + 1 :])
                contact = book.find_address(name)
                if contact:
                    if (
                        contact.address == old_address
                    ):  # Check if the old address matches
                        contact.address = new_address  # Change the address
                        print(
                            Colorizer.info(
                                f"Address changed from '{old_address}' to '{new_address}' for {name}."
                            )
                        )
                    else:
                        print(
                            Colorizer.error(
                                f"Error: Old address '{old_address}' not found for {name}."
                            )
                        )
                else:
                    print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "del_address":
                if not args:
                    print(Colorizer.error("Error: Input a name."))
                    continue
                name = args[0]
                contact = book.find_address(name)
                if contact:
                    contact.delete_address()
                else:
                    print(Colorizer.error(f"Error: Contact '{name}' not found."))

            elif command == "find_contact":
                if not args:
                    print(Colorizer.error("Error: Provide a name or phone number."))
                    continue

                search_term = args[0]
                contact = book.find_address(search_term)

                if contact:
                    print(Colorizer.info(f"Found contact: {contact}"))
                else:
                    print(
                        Colorizer.error(
                            f"Error: No contact found with '{search_term}'."
                        )
                    )

            elif command == "help":
                command_help()

            elif command == "add_note":
                title = input("Input the name of the note: ").strip()
                content = input("Input the content of the note: ")
                tags_input = input("Input tags separated by commas: ").strip()
                tags = tags_input.split(",") if tags_input else None
                notes_manager.add_note(title, content, tags)

            elif command == "change_note":
                title = input("Enter the title of the note to edit: ").strip()
                field = (
                    input("Enter the field to edit (title/content/tags): ")
                    .strip()
                    .lower()
                )

                if field in ["title", "content", "tags"]:
                    new_value = input(f"Enter the new value for {field}: ").strip()
                    if field == "tags":
                        new_value = new_value.split(",") if new_value else None
                    notes_manager.edit_note(title, field, new_value)
                else:
                    print(
                        Colorizer.error(
                            "Invalid field. Choose from 'title', 'content', or 'tags'."
                        )
                    )

            elif command == "show_all_notes":
                notes_manager.display_all_notes()

            elif command == "find_note_by_title":
                title = input("Enter the title of the note to find: ").strip()
                note = notes_manager.find_note_by_title(title)
                if note:
                    print(
                        Colorizer.info(
                            f"Title: {note.title}\nContent: {note.content}\nTags: {', '.join(note.tags) if note.tags else 'No tags'}"
                        )
                    )

            elif command == "find_note_by_tag":
                tag = input("Enter the tag to search for notes: ").strip().lower()
                notes_manager.find_notes_by_tag(tag)

            elif command == "del_note":
                title = input("Enter the title of the note to delete: ").strip()
                notes_manager.delete_note_by_title(title)

        else:
            print(Colorizer.error("Error: Invalid command. Please try again."))


if __name__ == "__main__":
    main()
