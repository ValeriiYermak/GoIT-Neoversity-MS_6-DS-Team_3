"""Module to manage notes within Personal Assistant bot"""
from storage import Storage
from notes import Note
from colorama import Fore
from prettytable import PrettyTable


class NotesManager:
    def __init__(self):
        self.notes = Storage.load_notes()

    def add_note(self, title, content, tags=None):
        new_note = Note(title=title, content=content, tags=tags)
        self.notes.append(new_note)
        Storage.save_notes(self.notes)
        # print(Fore.GREEN + "Note successfully added.")

    def edit_note(self, title, field, new_value):
        note = self.find_note_by_title(title)
        if note:
            setattr(note, field, new_value)
            Storage.save_notes(self.notes)
            # print(Fore.GREEN + f"Note with title '{title}' updated.")
        else:
            print(Fore.RED + "Note hasn't been found.")

    def delete_note_by_title(self, title):
        for note in self.notes:
            if note.title == title:
                self.notes.remove(note)
                Storage.save_notes(self.notes)
                print(Fore.GREEN + f"Note with title '{title}' deleted.")
                return
        print(Fore.RED + f"Note with title '{title}' hasn't been found.")

    def find_note_by_title(self, title):
        for note in self.notes:
            if note.title == title:
                return note
        print(Fore.RED + f"Note with title '{title}' hasn't been found.")
        return None

    def display_all_notes(self):
        if not self.notes:
            print(Fore.RED + "No notes to display.")
            return

        table = PrettyTable()
        table.field_names = ["Title", "Content", "Tags"]
        for note in self.notes:
            tags_formatted = ", ".join(note.tags) if note.tags else "Nothing..."
            table.add_row([note.title, note.content, tags_formatted])
        print(table)

    def find_notes_by_tag(self, tag):
        # Фільтруємо нотатки за тегом
        results = [
            note for note in self.notes if tag.lower() in [t.lower() for t in note.tags]
        ]

        if results:
            # Відображаємо результати у вигляді таблиці
            table = PrettyTable()
            table.field_names = ["Title", "Content", "Tags"]
            for note in results:
                tags_formatted = ", ".join(note.tags) if note.tags else "Nothing..."
                table.add_row([note.title, note.content, tags_formatted])
            print(Fore.GREEN + f"Notes with the following tag '{tag}' found:")
            print(table)
        else:
            print(Fore.RED + f"No notes with tag '{tag}' found.")

    def sort_notes_by_tag(self):
        sorted_notes = sorted(
            self.notes, key=lambda note: note.tags[0].lower() if note.tags else ""
        )

        if sorted_notes:
            # Відображення відсортованих нотаток у вигляді таблиці
            table = PrettyTable()
            table.field_names = ["Title", "Content", "Tags"]
            for note in sorted_notes:
                tags_formatted = ", ".join(note.tags) if note.tags else "Немає"
                table.add_row([note.title, note.content, tags_formatted])
            print(Fore.GREEN + "Notes sorted by tags:")
            print(table)
        else:
            print(Fore.RED + "No notes to sort.")
