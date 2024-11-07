from datetime import datetime, timedelta
from personal_helper.field import Field
from personal_helper.errors import input_error


class Birthday(Field):
    def __init__(self, value):
        self.value = self._validate_birthday(value)

    def _validate_birthday(self, value):
        try:
            # Check if the date is in the correct format
            datetime.strptime(value, "%d.%m.%Y")
            return value  # Return the validated date
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    @input_error
    @staticmethod
    def add_birthday_to_contact(name, birthday):
        name.add_birthday(birthday)
        return f"Birthday {birthday} added for {name}."

    @input_error
    @staticmethod
    def show_birthday_of_contact(name):
        if name.birthday:
            return f"{name.name.value}'s birthday is {name.birthday.value}."
        return f"{name.name.value} does not have a birthday set."

    def change_birthday(self, new_birthday):
        try:
            validate_birthday = self._validate_birthday(new_birthday)
            self.value = validate_birthday
            return f"Birthday for {self.name.value} changed to {self.value}."
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def remove_birthday(self):
        self.value = None

    @staticmethod
    def get_upcoming_birthdays(book, days_ahead):
        upcoming_birthdays = []
        today = datetime.now().date()
        target_date = today + timedelta(days=days_ahead)
        for contact in book.values():
            if contact.birthday:
                birthday = datetime.strptime(contact.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday.replace(year=today.year)
                # If birthday is in this year
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                # Check if birthday is upcoming
                if today <= birthday_this_year <= target_date:
                    upcoming_birthdays.append(
                        {
                            "name": contact.name.value,
                            "congratulation_date": birthday_this_year.strftime(
                                "%d.%m.%Y"
                            ),
                        }
                    )
        return upcoming_birthdays
