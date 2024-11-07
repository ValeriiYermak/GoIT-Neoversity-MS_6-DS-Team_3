from personal_helper.validators import normalize_phone
from personal_helper.field import Field


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
                    f"Invalid phone number: {number}. The number must have not less than 10 digits."
                )

    def add_phone(self, number):
        normalized_number = normalize_phone(number)
        if isinstance(normalized_number, str) and not normalized_number.startswith(
            "Invalid"
        ):
            if normalized_number not in self.value:
                self.value.append(normalized_number)
        else:
            raise ValueError(
                f"Invalid phone number: {number}. The number must have not less than 10 digits."
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
                        f"Invalid new phone number: {new_number}. The number must have not less than 10 digits."
                    )
        return False  # return False if the old number is not found

    def remove_phone(self, number):
        normalized_number = normalize_phone(number)
        if normalized_number in self.value:
            self.value.remove(normalized_number)  # remove the phone number
        else:
            print(f"Error: Phone number {number} not found.")
