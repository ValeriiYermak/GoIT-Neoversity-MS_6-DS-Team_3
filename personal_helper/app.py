from prompt_toolkit import PromptSession
#from prompt_toolkit.output import DummyOutput
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from console.colorizer import Colorizer, ColorizeType
from console.command_logger import write_command_log
import commands

# Define all available commands
COMMANDS = [
    "help", "hello", "exit", "close", "add-contact", "all-contacts", "change-contact",
    "find-contact", "delete-contact", "show-phone", "add-birthday", "show-birthday",
    "birthdays", "add-email", "show-email", "change-email", "delete-email", "add-address",
    "show-address", "delete-address", "add-note", "delete-note", "change-note",
    "find-note-by-title", "find-note-by-tag", "show-all-notes", "show-commands"
]

# Create a WordCompleter for autocompletion
command_completer = WordCompleter(COMMANDS, ignore_case=True)

# Main command loop
def main_loop():
    """
    Main command loop to handle user input and execute commands.
    """
    session = PromptSession(completer=command_completer)
    print(Colorizer.highlight("HERE IS YOUR PERSONAL HELPER."))
    commands.display_command_menu()  # Display the command menu at the start
    #session = PromptSession(completer=command_completer, output=DummyOutput())
    while True:
        try:
            user_input = session.prompt(HTML('<ansicyan>Enter command: </ansicyan>')).strip().split()
            command = user_input[0].lower()
            args = user_input[1:]
            write_command_log(" ".join(user_input))
            interpret_command(command, args)
        except (EOFError, KeyboardInterrupt):
            print(Colorizer.success("\nGoodbye!"))
            break

def interpret_command(command, args):
    """
    Interpret and execute the given command with arguments.
    """
    commands_dict = {
        'help': commands.command_help,
        'hello': commands.command_hello,
        'exit': commands.command_exit,
        'close': commands.command_exit,
        'add-contact': lambda: commands.command_add_contact(*args),
        'all-contacts': commands.command_all_contacts,
        'change-contact': lambda: commands.command_change_contact(*args),
        'find-contact': lambda: commands.command_find_contact(*args),
        'delete-contact': lambda: commands.command_delete_contact(*args),
        'show-phone': lambda: commands.command_show_phone(*args),
        'add-birthday': lambda: commands.command_add_birthday(*args),
        'show-birthday': lambda: commands.command_show_birthday(*args),
        'birthdays': lambda: commands.command_birthdays(*args),
        'add-email': lambda: commands.command_add_email(*args),
        'show-email': lambda: commands.command_show_email(*args),
        'change-email': lambda: commands.command_change_email(*args),
        'delete-email': lambda: commands.command_delete_email(*args),
        'add-address': lambda: commands.command_add_address(*args),
        'show-address': lambda: commands.command_show_address(*args),
        'delete-address': lambda: commands.command_delete_address(*args),
        'add-note': lambda: commands.command_add_note(*args),
        'delete-note': lambda: commands.command_delete_note(*args),
        'change-note': lambda: commands.command_change_note(*args),
        'find-note-by-title': lambda: commands.command_find_note_by_title(*args),
        'find-note-by-tag': lambda: commands.command_find_note_by_tag(*args),
        'show-all-notes': commands.command_show_all_notes,
        'show-commands': commands.command_show_commands,
    }
    if command in commands_dict:
        try:
            commands_dict[command]()
        except TypeError:
            print(Colorizer.error(f"Invalid arguments for command: {command}. Type 'help' for usage."))
    else:
        print(Colorizer.error(f"Unknown command: {command}. Type 'help' for a list of commands."))

# Start the main loop
if __name__ == "__main__":
    main_loop()