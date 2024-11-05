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
                raise ValueError(f"Invalid phone number: {number}. The number must have not less than 10 digits.")

    def add_phone(self, number):
        normalized_number = normalize_phone(number)
        if isinstance(normalized_number, str) and not normalized_number.startswith("Invalid"):
            if normalized_number not in self.value:
                self.value.append(normalized_number)
        else:
            raise ValueError(f"Invalid phone number: {number}. The number must have not less than 10 digits.")

    def find_phone(self, number):
        normalized_phone_number = normalize_phone(number)
        return normalized_phone_number in self.value

    def edit_phone(self, old_number, new_number):
        for index, num in enumerate(self.value):
            if num == normalize_phone(old_number):
                self.value[index] = normalize_phone(new_number)  # Оновлюємо значення
                return True
            return False

    def remove_phone(self):
        self.value = []