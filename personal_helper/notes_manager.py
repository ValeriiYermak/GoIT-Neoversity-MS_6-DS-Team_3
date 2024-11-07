from prettytable import PrettyTable
from colorama import Fore, Style
from storage import Storage

NOTES_FILE = "notes.json"

class Note:
    def __init__(self, content, tags=None):
        self.content = content
        self.tags = tags if tags else []

    def to_dict(self):
        return {"Content": self.content, "Tags": self.tags}

class NotesManager:
    def __init__(self):
        self.notes = self.load_notes()

    def load_notes(self):
        notes_data = Storage.load_data(NOTES_FILE)
        return [Note(**note) for note in notes_data]

    def save_notes(self):
        notes_data = [note.to_dict() for note in self.notes]
        Storage.save_data(notes_data, NOTES_FILE)

    def add_note(self, content, tags=None):
        new_note = Note(content, tags)
        self.notes.append(new_note)
        self.save_notes()
        print(Fore.GREEN + "Нотатку додано успішно!" + Style.RESET_ALL)

    def edit_note(self, index, new_content=None, new_tags=None):
        try:
            note = self.notes[index]
            if new_content: note.content = new_content
            if new_tags is not None: note.tags = new_tags
            self.save_notes()
            print(Fore.GREEN + "Нотатку оновлено успішно!" + Style.RESET_ALL)
        except IndexError:
            print(Fore.RED + "Нотатку не знайдено!" + Style.RESET_ALL)

    def delete_note(self, index):
        try:
            self.notes.pop(index)
            self.save_notes()
            print(Fore.GREEN + "Нотатку видалено успішно!" + Style.RESET_ALL)
        except IndexError:
            print(Fore.RED + "Нотатку не знайдено!" + Style.RESET_ALL)

    def show_notes(self):
        table = PrettyTable()
        table.field_names = ["Index", "Content", "Tags"]
        for i, note in enumerate(self.notes):
            table.add_row([i, note.content, ", ".join(note.tags)])
        print(table)

    def search_by_tag(self, tag):
        table = PrettyTable()
        table.field_names = ["Index", "Content", "Tags"]
        for i, note in enumerate(self.notes):
            if tag in note.tags:
                table.add_row([i, note.content, ", ".join(note.tags)])
        if table.rows:
            print(Fore.GREEN + f"Нотатки з тегом '{tag}':" + Style.RESET_ALL)
            print(table)
        else:
            print(Fore.YELLOW + f"Немає нотаток з тегом '{tag}'." + Style.RESET_ALL)
