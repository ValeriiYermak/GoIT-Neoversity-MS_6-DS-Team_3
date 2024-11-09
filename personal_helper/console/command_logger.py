COMMANDS_LOG_FILE = 'commands.log'

def read_commands_log():
    """
    Read commands from the log file.
    """
    try:
        with open(COMMANDS_LOG_FILE, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def write_command_log(command):
    """
    Write a command to the log file.
    """
    with open(COMMANDS_LOG_FILE, 'a') as file:
        file.write(command + '\n')