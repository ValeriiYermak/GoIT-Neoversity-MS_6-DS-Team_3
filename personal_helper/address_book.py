from collections import UserDict
from personal_helper.validators import normalize_phone
from personal_helper.phone import Phone
from personal_helper.birthday import Birthday
from personal_helper.field import Field
from personal_helper.email import Email



class AddressBook(UserDict):
    def add_address(self, address):
        if isinstance(address.name.value, str):
            self.data[address.name.value] = address
        else:
            raise TypeError("Contact name must be a string.")

    def add_contact(self, name, phones, birthday=None, email=None):
        for phone in phones:
            normalized_number = normalize_phone(phone)
            if not isinstance(normalized_number, str) and len(normalized_number) < 10:
                raise ValueError(f"Invalid phone number: {phone}. The number must have not less than 10 digits.")

        new_address = Record(name, phones, birthday, email)
        self.data[name.value] = new_address

    def find_address(self, query):
        # Перевіряємо, чи це ім'я (алфавітні символи) або телефонний номер
        if query.isdigit() or query.startswith("+"):
            normalized_number = normalize_phone(query)  # Нормалізуємо номер для пошуку
            for record in self.data.values():
                for phone in record.phones:
                    if normalized_number in phone.value:
                        return record
        else:
            # Пошук за ім'ям
            return self.data.get(query, None)
        return None

    def edit_address(self, name, new_address):
        self.data[name] = new_address

    def delete_address(self, name):
        if name in self.data:
            del self.data[name]


class Record:
    def __init__(self, name, phones=None, birthday=None, email=None):
        self.name = Name(name)
        self.phones = Phone(phones) if phones else Phone()  # Якщо телефони не передані, створити пустий Phone
        self.email = email
        if birthday:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = None


    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_record(self, phones):
        for number in phones:
            normalized_number = normalize_phone(number)
            if normalized_number:
                self.phones.add_phone(normalized_number)  # Використовуємо метод add_phone

    def find_record(self, phones):
        for phone in self.phones:
            if phone.find_phone(normalize_phone(phones)):
                return phone.value
        return None

    def edit_record(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.find_phone(normalize_phone(old_phone)):
                phone.edit_phone(old_phone, new_phone)
                return True
        return False

    def add_email(self, email):
        self.email = email


    def remove_record(self, phones):
        self.phones = [phone for phone in self.phones if not phone.find_phone(normalize_phone(phones))]

    def __str__(self):
        phones = ', '.join(self.phones.value) if self.phones else ''
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        email = f", email: {self.email}" if self.email else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday_str}{email}"

class Name(Field):
    pass