"""
This module contains the Phone class, which represents a phone number for a contact.

Attributes:
    numbers (list): A list of phone numbers.
    value (list): A list of normalized phone numbers.

Methods:
    _normalize_all_phones(self): Normalizes all phone numbers in the numbers list and adds them to the value list.
    __iter__(self): Returns an iterator over the value list.
    add_phone(self, number): Adds a phone number to the value list.
    find_phone(self, number): Returns True if the phone number is in the value list, False otherwise.
    edit_phone(self, old_number, new_number): Replaces the old phone number with the new one in the value list.
    remove_phone(self, number): Removes the phone number from the value list.

Classes:
    Phone: A class that represents a phone number for a contact.
"""


from validators import normalize_phone
from field import Field
from colorizer import Colorizer


class Phone(Field):
    def __init__(self, phones=None):
        self.numbers = list(phones) if phones else []
        self.value = []
        self._normalize_all_phones()

    def _normalize_all_phones(self):
        for number in self.numbers:
            normalized_phone = normalize_phone(number)
            if isinstance(normalized_phone, str):
                self.value.append(normalized_phone)
            else:
                raise ValueError(
                    Colorizer.error(
                        f"Invalid phone number: {number}. The number must have not less than 10 digits."
                    )
                )

    def __iter__(self):
        return iter(self.value)

    def add_phone(self, number):
        normalized_number = normalize_phone(number)
        if isinstance(normalized_number, str) and not normalized_number.startswith(
            "Invalid"
        ):
            if normalized_number not in self.value:
                self.value.append(normalized_number)
        else:
            raise ValueError(
                Colorizer.error(
                    f"Invalid phone number: {number}. The number must have not less than 10 digits."
                )
            )

    def find_phone(self, number):
        normalized_phone_number = normalize_phone(number)
        return normalized_phone_number in self.value

    def edit_phone(self, old_number, new_number):
        for index, num in enumerate(self.value):
            if num == normalize_phone(old_number):
                normalized_new_number = normalize_phone(new_number)
                if isinstance(
                    normalized_new_number, str
                ) and not normalized_new_number.startswith("Invalid"):
                    self.value[index] = normalized_new_number
                    return True
                else:
                    raise ValueError(
                        Colorizer.error(
                            f"Invalid new phone number: {new_number}. The number must have not less than 10 digits."
                        )
                    )
        return False  # return False if the old number is not found

    def remove_phone(self, number):
        normalized_number = normalize_phone(number)
        if normalized_number in self.value:
            self.value.remove(normalized_number)  # remove the phone number
        else:
            print(Colorizer.error(f"Error: Phone number {number} not found."))
