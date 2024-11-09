from collections import UserDict
from personal_helper.validators import normalize_phone
from personal_helper.phone import Phone
from personal_helper.birthday import Birthday
from personal_helper.field import Field
import re


class AddressBook(UserDict):
    def add_address(self, address):
        if isinstance(address.name.value, str):
            self.data[address.name.value] = address
        else:
            raise TypeError("Contact name must be a string.")

    def add_contact(self, name, phones, birthday=None, email=None, address=None):
        for phone in phones:
            normalized_number = normalize_phone(phone)
            if not isinstance(normalized_number, str) and len(normalized_number) < 10:
                raise ValueError(
                    f"Invalid phone number: {phone}. The number must have not less than 10 digits."
                )

        new_address = Record(name, phones, birthday, email, address)
        self.data[name.value] = new_address
        print(f"Contact added: {new_address}")

    def find_address(self, query):
        # Checks if the query is a phone number
        if query.isdigit() or query.startswith("+"):
            normalized_number = normalize_phone(query)  # Normalize the phone number
            for record in self.data.values():
                for phone in record.phones:
                    if normalized_number in phone.value:
                        return record
        else:
            # Find the address by name
            return self.data.get(query, None)
        return None

    def edit_address(self, name, new_address):
        self.data[name] = new_address

    def update_address(self, name, old_address, new_address):
        contact = self.data.get(name)
        if contact:
            contact.change_address(old_address, new_address)
        else:
            print(f"Error: Contact '{name}' not found.")

    def delete_contact(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def delete_address(self, name):
        contact = self.data.get(name)
        if contact:
            contact.delete_address()
            print(f"Address removed from contact {name}.")
        else:
            print(f"Error: Contact {name} not found.")

    def change_address(self, name, new_address):
        contact = self.data.get(name)
        if contact:
            contact.change_address(new_address)
        else:
            print(f"Error: Contact {name} not found.")

    def delete_phone(self, name, phone_number):
        if name in self.data:
            contact = self.data[name]
            if contact.phones.find_phone(phone_number):
                contact.delete_phone(phone_number)
                return True
            else:
                print(f"Error: Phone number '{phone_number}' not found for contact '{name}'.")
        else:
            print(f"Error: Contact '{name}' not found.")
        return False

    def delete_birthday(self, name):
        if name in self.data:
            contact = self.data[name]
            contact.delete_birthday()
        else:
            print(f"Error: Contact '{name}' not found.")

    def change_name(self, old_name, new_name):
        old_name = old_name.strip().lower()
        new_name = new_name.strip()
        for contact in self.data.values():
            if contact.name.value.lower() == old_name:
                contact.name.value = new_name
                print(f"Name changed from {(old_name.title())} to {new_name}")
                return
        print(f"Error: Contact '{old_name}' not found.")



class Record:
    def __init__(self, name, phones=None, birthday=None, email=None, address=None):
        self.name = Name(name)
        self.phones = (
            Phone(phones) if phones else Phone()
        )  # If the list of phones is empty, create an empty list
        self.birthday = Birthday(birthday) if birthday else None
        self.email = Email(email) if email else None
        self.address = address

    def add_email(self, email):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            print(
                "Error: Invalid email format. Please enter a valid email email@domain.com"
            )
            return

        if self.email and self.email.email == email:
            print(f"Email {email} is already added to {self.name.value}.")
            return

        # initialize the email
        if not isinstance(self.email, Email):
            self.email = Email(email)
        else:
            self.email.email = email  # replace the old email with the new one

        print(f"Emil {email} added to {self.name.value}.")

    def change_email(self, new_email):
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", new_email):
            self.email = new_email
            print(f"Email successfully updated to {new_email}.")
        else:
            print("Error: Invalid email format. Use email@domain.com.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def change_birthday(self, new_birthday):
        # Checks if the new birthday is in the correct format
        if re.match(r"^\d{2}\.\d{2}\.\d{4}$", new_birthday):
            self.birthday = new_birthday
            print(f"Birthday successfully updated to {new_birthday}.")
        else:
            print("Error: Invalid birthday format. Expected DD.MM.YYYY.")

    def add_number(self, phones):
        for number in phones:
            normalized_number = normalize_phone(number)
            if normalized_number:
                self.phones.add_phone(
                    normalized_number
                )  # Use the Phone class to add the phone number

    def find_number(self, phones):
        for phone in self.phones:
            if phone.find_phone(normalize_phone(phones)):
                return phone.value
        return None

    def edit_number(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.find_phone(normalize_phone(old_phone)):
                phone.edit_phone(old_phone, new_phone)
                return True
        return False

    def remove_number(self, phones):
        self.phones = [
            phone
            for phone in self.phones
            if not phone.find_phone(normalize_phone(phones))
        ]

    def delete_phone(self, phone_number):
        if self.phones.find_phone(phone_number):
            self.phones.remove_phone(
                phone_number
            )  # Use the Phone class to remove the phone number
        else:
            print(f"Error: Phone number {phone_number} not found for {self.name}.")

    def add_address(self, address):
        self.address = address

    def change_address(self, name, new_address):
        contact = self.data.get(name)
        if contact:
            old_address = contact.address
            if old_address == new_address:
                print(
                    f"Error: The new address is the same as the old address: '{old_address}'. No changes needed."
                )
            else:
                contact.address = new_address
                print(
                    f"Address changed from '{old_address}' to '{new_address}' for {name}."
                )
        else:
            print(f"Error: Contact {name} not found.")

    def delete_address(self):
        if self.address:
            removed_address = self.address
            self.address = None
            print(
                f"Address '{removed_address}' for '{self.name.value}' has been removed."
            )
        else:
            print(f"Error: No address to remove for {self.name.value}.")

    def delete_birthday(self):
        if self.birthday:
            self.birthday = None
            print(f"Birthday for {self.name.value} has been removed.")
        else:
            print(f"Error: No birthday to remove for {self.name.value}.")

    def __str__(self):
        phones = ", ".join(self.phones.value) if self.phones else ""
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        email_str = f", email: {str(self.email)}" if self.email else ""
        address = f", address: {self.address}" if self.address else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday_str}{email_str}{address}"


class Email:
    def __init__(self, email=None):
        self.email = email  # Initialize email with None if not provided

    def __str__(self):
        return (
            self.email if self.email else "No email"
        )  # Return "No email" if email is None

    @staticmethod
    def find_email(contact):
        return contact.email if contact.email else "No email found"

    def remove_email(contact, email):
        if contact.email and contact.email.email == email:
            contact.email = None
            return True
        return False


class Name(Field):
    pass
