import json
from notes import Note
from colorama import Fore

NOTES_FILE = "notes.json"


class Storage:
    @staticmethod
    def save_notes(notes, filename=NOTES_FILE):
        data = [
            {"title": note.title, "content": note.content, "tags": note.tags}
            for note in notes
        ]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        # print(Fore.GREEN + "Note successfully stored.")

    @staticmethod
    def load_notes(filename=NOTES_FILE):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                # Перевірка ключів даних для відладки
                print("Notes data loaded:", data)
                # Переконайтеся, що ключі 'title', 'content' і 'tags' існують
                return [Note(**note_data) for note_data in data]
        except FileNotFoundError:
            print(Fore.RED + "No JSON file with notes found. Creating a new file...")
            return []
        except TypeError as e:
            print(Fore.RED + f"JSON format error: {e}")
            return []
