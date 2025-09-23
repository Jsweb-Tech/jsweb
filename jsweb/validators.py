import re

class ValidationError(Exception):
    """Raised when a validator fails to validate its input."""
    def __init__(self, message="Invalid input."):
        super().__init__(message)

class DataRequired:
    """Checks that the field is not empty."""
    def __init__(self, message="This field is required."):
        self.message = message

    def __call__(self, form, field):
        if not field.data or not field.data.strip():
            raise ValidationError(self.message)

class Email:
    """Checks for a valid email format."""
    def __init__(self, message="Invalid email address."):
        self.message = message
        self.regex = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

    def __call__(self, form, field):
        if not self.regex.match(field.data):
            raise ValidationError(self.message)

class Length:
    """Checks that the field's length is within a specified range."""
    def __init__(self, min=-1, max=-1, message=None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        length = len(field.data) if field.data else 0
        if length < self.min or (self.max != -1 and length > self.max):
            if self.message:
                message = self.message
            elif self.max == -1:
                message = f"Field must be at least {self.min} characters long."
            elif self.min == -1:
                message = f"Field cannot be longer than {self.max} characters."
            else:
                message = f"Field must be between {self.min} and {self.max} characters long."
            raise ValidationError(message)

class EqualTo:
    """Compares the values of two fields."""
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(f"Invalid field name '{self.fieldname}'.")
        if field.data != other.data:
            message = self.message
            if message is None:
                message = f"Field must be equal to {self.fieldname}."
            raise ValidationError(message)
