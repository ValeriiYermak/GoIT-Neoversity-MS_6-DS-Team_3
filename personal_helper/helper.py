import re
import pickle
from personal_helper.validators import normalize_phone
from personal_helper.contact_book import AddressBook, Record
from personal_helper.birthday import Birthday
from personal_helper.contact_book import Email


def parse_input(user_input):
    if not user_input.strip():
        print("Error: No command entered.")
        return None, []  # Return None for both cmd and args

    parts = user_input.strip().split()
    cmd = parts[0].strip().lower()  # Choose the first word as the command

    args = parts[1:]  # Remove the command from the list of arguments
    return cmd, args


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break

        elif command == "hello":  # HELLO #
            print("How can I help you?")

        elif command == "add":  # ADD #
            if len(args) < 2:
                print("Error: Input requires at least two arguments: name and phone.")
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
                        print(f"Warning: Ignoring additional phone number {arg}.")
                elif re.match(r"\d{2}\.\d{2}\.\d{4}$", arg):  # check if it's a birthday
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
                    f"Error: Invalid phone number '{phone}'. Expected format: 10 to 13 digits."
                )  # Show the error message
                continue  # Missing or invalid phone number
            contact = book.find_address(name)
            if contact:
                if normalized_phone:
                    contact.phones.add_phone(normalized_phone)  # add the primary phone
                    print(f"Phone number {normalized_phone} added to {name}.")
                if phone2:
                    normalized_phone2 = normalize_phone(phone2)
                    if isinstance(
                        normalized_phone2, str
                    ) and not normalized_phone2.startswith("Invalid"):
                        contact.phones.add_phone(
                            normalized_phone2
                        )  # Add the secondary phone
                        print(f"Phone number {normalized_phone2} added to {name}.")
                    else:
                        print(f"Warning: Ignoring additional phone number {phone2}.")
                if birthday:
                    if re.match(
                        r"^\d{2}\.\d{2}\.\d{4}$", birthday
                    ):  # Check the format of the birthday
                        contact.add_birthday(birthday)  # Add the birthday
                        print(f"Birthday {birthday} added to {name}.")
                    else:
                        print("Error: Invalid birthday format. Expected DD.MM.YYYY.")
                if email:
                    if re.match(
                        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email
                    ):
                        contact.add_email(email)
                        print(f"Email {email} added to {name}.")
                    else:
                        print("Error: Invalid email format. Use email@domain.com.")
                    continue
                if address:
                    contact.address = address  # Add the address if it exists
                    print(f"Address {address} added to {name}.")
            else:
                # Create a new record if the contact doesn't exist
                phones = [phone]
                if phone2:
                    phones.append(phone2)  # Add the second phone number if it exists
                record = Record(
                    name, phones, birthday, email, address
                )  # Given name, phones, birthday, email, address
                book.add_address(record)
                print(
                    f"New contact {name} added with phone number: {phone}, "
                    f"second phone number: {phone2 if phone2 else 'N/A'}, "
                    f"birthday: {birthday if birthday else 'N/A'}, "
                    f"email: {email if email else 'N/A'}, "
                    f"and address: {address if address else 'N/A'}."
                )

        elif command == "change_name":
            if len(args) < 2 or "|" not in " ".join(args):
                print("Error: Provide old name and new name.")
                continue
            full_input = " ".join(args)
            if "|" not in full_input:
                print("Error: Provide old name and new name.")
                continue
            old_name, new_name = full_input.split("|", 1)
            old_name = old_name.strip()
            new_name = new_name.strip()

            if old_name and new_name:
                book.change_name(old_name, new_name)
            else:
                print("Error: Provide both old name and new name.")  # Change name

        elif command == "change_phone":  # Change phone number
            if len(args) < 3:
                print("Error: Provide name, old phone, and new phone.")
            else:
                name, old_phone, new_phone = args
                contact = book.find_address(name)
                if contact:
                    # Normalize the new phone number
                    normalized_new_phone = normalize_phone(new_phone)

                    if contact.phones.edit_phone(old_phone, normalized_new_phone):
                        print(
                            f"Phone number changed from {old_phone} to {normalized_new_phone} for {name}."
                        )
                    else:
                        print(f"Phone number {old_phone} not found for {name}.")
                else:
                    print(f"Error: Contact '{name}' not found.")

        elif command == "show_phone":  # Find phone number
            if not args:
                print("Error: Provide a name.")
            else:
                name = args[0]
                contact = book.find_address(name)
                if contact:
                    print(f"{name}'s phone numbers: {', '.join(contact.phones.value)}")
                else:
                    print(f"Error: Contact '{name}' not found.")

        elif command == "del_phone":  # Delete phone number from contact
            try:
                name = args[0]
                phone_number = args[1]  # Use the second argument as the phone number
                if not name or not phone_number:
                    print("Error: Both contact name and phone number are required.")
                    continue
            except IndexError:
                print("Error: Both contact name and phone number are required.")
                continue
            if book.delete_phone(name, phone_number):
                print(f"Phone number '{phone_number}' deleted from contact '{name}'.")
            else:
                print(
                    f"Error: Contact '{name}' or phone number '{phone_number}' not found."
                )

        elif command == "show_all":
            if not book.data:
                print("No contacts found.")
            else:
                for contact in book.values():
                    print(contact)

        elif command == "del_contact":  # Delete contact
            if not args:
                print("Error: Input the contact name to delete.")
                continue
            name = args[0]
            if book.delete_contact(name):
                print(f"Contact '{name}' deleted.")
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "add_birthday":  # Add birthday
            if not args or len(args) < 2:
                print("Error: Input name and birthday.")
                continue
            name, birthday = args[0], args[1]
            contact = book.find_address(name)
            if contact:
                # check birthday format
                if re.match(r"\d{2}\.\d{2}\.\d{4}$", birthday):
                    Birthday.add_birthday_to_contact(contact, birthday)
                    print(f"Birthday {birthday} added to {name}.")
                else:
                    print(f"Error: Invalid birthday format. Expected DD.MM.YYYY.")
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "show_birthday":  # Show birthday
            if not args:
                print("Error:Input a name.")
                continue
            name = args[0]
            contact = book.find_address(name)
            if contact:
                print(Birthday.show_birthday_of_contact(contact))
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "change_birthday":  # Change birthday
            if not args:
                print("Error: Input a name and new birthday.")
                continue
            name = args[0]
            if len(args) < 2:
                print(
                    "Error: You must provide a new birthday in the format DD.MM.YYYY."
                )
                continue
            new_birthday = args[1]

            # Validate the new birthday format
            if not re.match(r"^\d{2}\.\d{2}\.\d{4}$", new_birthday):
                print("Error: Invalid birthday format. Expected DD.MM.YYYY.")
                continue

            contact = book.find_address(name)
            if contact:
                contact.add_birthday(
                    new_birthday
                )  # Replace the old birthday with the new one
                print(f"Birthday of {name} changed to {new_birthday}.")
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "show_birthdays":
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
                print("Error: Input a name.")
                continue
            name = args[0]
            if book.delete_birthday(name):
                print(f"Birthday of {name} deleted.")
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "add_email":
            if not args or len(args) < 2:
                print("Error: Input name and email.")
                continue
            name, email = args[0], args[1]
            contact = book.find_address(name)
            if contact:
                if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                    contact.add_email(email)
                else:
                    print("Error: Invalid email format. Use email@domain.com")

        elif command == "show_email":  # Show email
            if not args:
                print("Error:Input a name.")
                continue
            name = args[0]
            contact = book.find_address(name)
            if contact:
                print(Email.find_email(contact))
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "change_email":
            if not args:
                print("Error: Input name and email.")
                continue
            name = args[0]
            if len(args) < 2:
                print("Error: You must provide a new email. Use email@domain.com")
                continue
            new_email = args[1]
            contact = book.find_address(name)
            if contact:
                if re.match(
                    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", new_email
                ):
                    contact.add_email(new_email)
                else:
                    print("Error: Invalid email format. Use email@domain.com")

        elif command == "del_email":  # Delete email
            if not args or len(args) < 2:
                print("Error: Input name and email.")
                continue
            name, email = args[0], args[1]
            contact = book.find_address(name)
            if contact:
                if Email.remove_email(contact, email):
                    print(f"Email {email} deleted from {name}.")
                else:
                    print(f"Error: Email {email} not found for {name}.")
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "add_address":
            if not args or len(args) < 2:
                print("Error: Input name and address.")
                continue
            name = args[0]
            address = " ".join(args[1:]).strip()
            contact = book.find_address(name)
            if contact:
                contact.add_address(address)  # Add the address
                print(f"Address '{address}' added to '{name}'.")
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "show_address":  # Show email
            if not args:
                print("Error:Input a name.")
                continue
            name = args[0]
            contact = book.find_address(name)
            if contact:
                if contact.address:
                    print(f"Address for {name}: {contact.address}")
                else:
                    print(f"Error: Contact '{name}' has no address.")
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "change_address":  # Change address
            if len(args) < 3 or "|" not in args:
                print("Error: Provide name, old address, |, and new address.")
                continue
            separator_index = args.index("|")
            name = args[0]
            old_address = " ".join(args[1:separator_index])
            new_address = " ".join(args[separator_index + 1 :])
            contact = book.find_address(name)
            if contact:
                if contact.address == old_address:  # Check if the old address matches
                    contact.address = new_address  # Change the address
                    print(
                        f"Address changed from '{old_address}' to '{new_address}' for {name}."
                    )
                else:
                    print(f"Error: Old address '{old_address}' not found for {name}.")
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "del_address":
            if not args:
                print("Error: Input a name.")
                continue
            name = args[0]
            contact = book.find_address(name)
            if contact:
                contact.delete_address()
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "help":
            print("Available commands:")
            print('  "add_phone" - add a new contact')
            print('  "add_birthday" - add a birthday to a contact')
            print('  "add_email" - add an email to a contact')
            print('  "add_address" - add a address to a contact')

            print('  "show_all" - show all contacts')
            print('  "show_phone" - show a phone number')
            print('  "show_birthday" - show a birthday of a contact')
            print('  "show_email" - show an email of a contact')
            print('  "show_address" - show a address for contact')
            print('  "show_birthdays" - show upcoming birthdays')

            print('  "change_name" - change a contact name')
            print('  "change_phone" - change a phone number')
            print('  "change_birthday" - change a birthday of a contact')
            print('  "change_email" - change an email of a contact')
            print('  "change_address" - change a address for contact')

            print('  "del_contact" - remove a contact')
            print('  "del_phone" - remove a phone from contact')
            print('  "del_birthday" - remove a birthday from a contact')
            print('  "del_email" - remove a email from a contact')
            print('  "del_address" - remove a address from contact')

            print('  "help" - show this help message')
            print('  "exit"/"cancel" - exit the program')

        else:
            print("Error: Invalid command. Please try again.")
