from colorama import Fore, Style, init


class ColorizeType:
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    HIGHLIGHT = "highlight"
    COMMANDLINE = "commandline"


class Colorizer:
    """
    Colorize text output with colorama
    """

    init()

    INFO = Fore.WHITE
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    SUCCESS = Fore.GREEN
    HIGHLIGHT = Fore.CYAN

    @staticmethod
    def colorize(text, color_type):
        # Get the corresponding color code
        color_code = getattr(Colorizer, color_type.upper(), Fore.RESET)
        # Return the text with the set color and reset style
        return f"{color_code}{text}{Style.RESET_ALL}"

    @staticmethod
    def info(text):
        return Colorizer.colorize(text, ColorizeType.INFO)

    @staticmethod
    def warn(text):
        return Colorizer.colorize(text, ColorizeType.WARNING)

    @staticmethod
    def error(text):
        return Colorizer.colorize(text, ColorizeType.ERROR)

    @staticmethod
    def success(text):
        return Colorizer.colorize(text, ColorizeType.SUCCESS)

    @staticmethod
    def highlight(text):
        return Colorizer.colorize(text, ColorizeType.HIGHLIGHT)
