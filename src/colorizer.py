from colorama import Fore, Style, init

# Define a class for categorizing different types of messages.
class ColorizeType:
    # Different types of message categories
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    HIGHLIGHT = "highlight"
    COMMANDLINE = "commandline"


# Class responsible for adding colors to text output using colorama.
class Colorizer:
    """
    Colorize text output with colorama
    """
    
    # Initialize colorama to work with color codes
    init()
    
    # Define color mapping for different message types
    INFO = Fore.WHITE
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    SUCCESS = Fore.GREEN
    HIGHLIGHT = Fore.CYAN

    @staticmethod
    def colorize(text, color_type):
        # Get the corresponding color code for the message type. Default to resetting if unknown type.
        color_code = getattr(Colorizer, color_type.upper(), Fore.RESET)
        # Return the text decorated with the color and reset style at the end
        return f"{color_code}{text}{Style.RESET_ALL}"

    @staticmethod
    def info(text):
        # Colorize an INFO type message
        return Colorizer.colorize(text, ColorizeType.INFO)

    @staticmethod
    def warn(text):
        # Colorize a WARNING type message
        return Colorizer.colorize(text, ColorizeType.WARNING)

    @staticmethod
    def error(text):
        # Colorize an ERROR type message
        return Colorizer.colorize(text, ColorizeType.ERROR)

    @staticmethod
    def success(text):
        # Colorize a SUCCESS type message
        return Colorizer.colorize(text, ColorizeType.SUCCESS)

    @staticmethod
    def highlight(text):
        # Colorize a HIGHLIGHT type message
        return Colorizer.colorize(text, ColorizeType.HIGHLIGHT)