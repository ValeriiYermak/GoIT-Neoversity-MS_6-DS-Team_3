"""Error handling."""

from colorizer import Colorizer


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return Colorizer.error(f"An unexpected error occurred: {str(e)}")

    return wrapper
