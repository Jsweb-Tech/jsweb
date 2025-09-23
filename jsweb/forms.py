from .validators import ValidationError

class Field:
    """A single field in a form."""
    def __init__(self, label=None, validators=None, default=""):
        self.label = label
        self.validators = validators or []
        self.data = None
        self.default = default
        self.errors = []

    def validate(self, form):
        """Validate the field by running all its validators."""
        self.errors = []
        for validator in self.validators:
            try:
                validator(form, self)
            except ValidationError as e:
                self.errors.append(str(e))
        return not self.errors

    def __call__(self, **kwargs):
        """Render the field as an HTML input."""
        kwargs.setdefault('id', self.name)
        kwargs.setdefault('name', self.name)
        kwargs.setdefault('type', 'text')
        if self.data:
            kwargs.setdefault('value', self.data)
        else:
            kwargs.setdefault('value', self.default)
        
        attributes = ' '.join(f'{key}="{value}"' for key, value in kwargs.items())
        return f'<input {attributes}>'

class StringField(Field):
    pass

class PasswordField(Field):
    def __call__(self, **kwargs):
        kwargs['type'] = 'password'
        return super().__call__(**kwargs)

class HiddenField(Field):
    def __call__(self, **kwargs):
        kwargs['type'] = 'hidden'
        return super().__call__(**kwargs)

class Form:
    """A collection of fields that can be validated together."""
    def __init__(self, formdata=None):
        self.formdata = formdata or {}
        self._fields = {}

        # Collect all Field instances from the class definition
        for name in dir(self):
            if isinstance(getattr(self, name), Field):
                field = getattr(self, name)
                field.name = name
                self._fields[name] = field
                # Populate field data from formdata if available
                if name in self.formdata:
                    field.data = self.formdata[name]

    def validate(self):
        """Validate all fields in the form."""
        success = True
        for name, field in self._fields.items():
            if not field.validate(self):
                success = False
        return success

    def __getitem__(self, name):
        return self._fields.get(name)
