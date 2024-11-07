import re
import pickle
from personal_helper.validators import normalize_phone
from personal_helper.address_book import AddressBook, Record
from personal_helper.birthday import Birthday




def parse_input(user_input):
    parts = user_input.split()
    cmd = parts[0].strip().lower()
    args = parts[1:]  # Отримати всі аргументи як плоский список
    return cmd, args


def load_data(filename = 'addressbook.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def save_data(book, filename = 'addressbook.pkl'):
    with open(filename,'wb') as f:
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

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":

            if len(args) < 2:
                print("Error: Input requires at least two arguments: name and phone.")
                continue

            name = args[0]
            phone = args[1]
            phone2 = None
            birthday = None
            email = None

            # Проходимо через всі аргументи і призначаємо їх відповідним полям
            for arg in args[2:]:
                if re.match(r"^\d{10,13}$", arg):  # Перевіряємо, чи це телефонний номер
                    if not phone2:
                        phone2 = arg  # Призначаємо другий номер
                    else:
                        print(f"Warning: Ignoring additional phone number {arg}.")
                elif re.match(r"\d{2}\.\d{2}\.\d{4}$", arg):  # Перевіряємо формат дати
                    birthday = arg
                elif re.match(r"[^@]+@[^@]+\.[^@]+", arg):  # Перевіряємо формат електронної пошти
                    email = arg
                else:
                    print(f"Warning: Ignoring invalid argument '{arg}'.")
            # Перевірка на валідність основного номера телефону
            normalized_phone = normalize_phone(phone)
            if isinstance(normalized_phone, str) and normalized_phone.startswith("Invalid"):
                print(normalized_phone)  # Виводимо повідомлення про помилку
                continue  # Пропускаємо ітерацію, не створюючи контакт
            # Виконання логіки для додавання або оновлення контакту
            contact = book.find_address(name)
            if contact:
                if normalized_phone:
                    contact.phones.add_phone(normalized_phone)  # Додаємо обов'язковий номер
                    print(f'Phone number {normalized_phone} added to {name}.')
                if phone2:
                    normalized_phone2 = normalize_phone(phone2)
                    if isinstance(normalized_phone2, str) and not normalized_phone2.startswith("Invalid"):
                        contact.phones.add_phone(normalized_phone2)  # Додаємо другий номер, якщо є
                        print(f'Phone number {normalized_phone2} added to {name}.')
                    else:
                        print(f"Warning: Ignoring additional phone number {phone2}.")
                if birthday:
                    if re.match(r"^\d{2}\.\d{2}\.\d{4}$", birthday):  # Перевірка формату дати
                        contact.add_birthday(birthday)  # Додаємо день народження, якщо формат правильний
                        print(f'Birthday {birthday} added to {name}.')
                    else:
                        print("Error: Invalid birthday format. Expected DD.MM.YYYY.")
                if email:
                    contact.email = email  # Додаємо email, якщо є
                    print(f'Email {email} added to {name}.')
            else:
                # Створюємо новий контакт з обов'язковими та опційними параметрами
                phones = [phone]
                if phone2:
                    phones.append(phone2)  # Додаємо другий номер, якщо є
                record = Record(name, phones, birthday, email)  # Передаємо список телефонів
                book.add_address(record)
                print(f"New contact {name} added with phone number {phone}, "
                      f"second phone number {phone2 if phone2 else 'N/A'}, "
                      f"birthday {birthday if birthday else 'N/A'}, "
                      f"and email {email if email else 'N/A'}.")


        elif command == "change":
            if len(args) < 3:
                print("Error: Provide name, old phone, and new phone.")
            else:
                name, old_phone, new_phone = args
                contact = book.find_address(name)
                if contact:
                    # Нормалізація старого і нового номера телефону
                    normalized_new_phone = normalize_phone(new_phone)  # Викликаємо функцію

                    if contact.phones.edit_phone(old_phone, normalized_new_phone):
                        print(f"Phone number changed from {old_phone} to {normalized_new_phone} for {name}.")
                    else:
                        print(f"Phone number {old_phone} not found for {name}.")
                else:
                    print(f"Error: Contact '{name}' not found.")


        elif command == "phone":
            if not args:
                print("Error: Provide a name.")
            else:
                name = args[0]
                contact = book.find_address(name)
                if contact:
                    print(f"{name}'s phone numbers: {', '.join(contact.phones.value)}")
                else:
                    print(f"Error: Contact '{name}' not found.")

        elif command == "all":
            if not book.data:
                print("No contacts found.")
            else:
                for contact in book.values():
                    print(contact)

        elif command == "add_birthday":
            if not args or len(args) < 2:
                print("Error: Input name and birthday.")
                continue

            name, birthday = args[0], args[1]
            contact = book.find_address(name)

            if contact:
                # Перевірка правильності формату дати за допомогою регулярного виразу
                if re.match(r"\d{2}\.\d{2}\.\d{4}$", birthday):
                    Birthday.add_birthday_to_contact(contact, birthday)
                    print(f'Birthday {birthday} added to {name}.')
                else:
                    print(f"Error: Invalid birthday format. Expected DD.MM.YYYY.")
            else:
                print(f"Error: Contact '{name}' not found.")


        elif command == "show_birthday":
            if not args:
                print('Error:Input a name.')
                continue
            name = args[0]
            contact = book.find_address(name)
            if contact:
                print(Birthday.show_birthday_of_contact(contact))
            else:
                print(f"Error: Contact '{name}' not found.")

        elif command == "birthdays":
            upcoming_birthdays = Birthday.get_upcoming_birthdays(book)
            if upcoming_birthdays:
                print('Upcoming birthdays:')
                for ub in upcoming_birthdays:
                    print(f'{ub['name']} on {ub['congratulation_date']}.')
            else:
                print('There are no upcoming birthdays.')

        else:
            print(f"Unknown command '{command}'.")
