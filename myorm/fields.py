"""myorm fields module."""


class BaseField:
    """Base field."""

    def __init__(self, value=None):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val


class IntegerField(BaseField):
    """Integer field."""


class CharField(BaseField):
    """Char field."""


class BooleanField(BaseField):
    """Boolean field."""

    def to_python(self):
        return bool(self.value)


class DateTimeField(BaseField):
    """Date and time field."""
