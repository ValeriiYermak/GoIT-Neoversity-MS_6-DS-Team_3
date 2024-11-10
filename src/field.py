"""
this is the base class for all fields
"""

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
