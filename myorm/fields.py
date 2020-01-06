"""myorm fields module."""


class BaseField:
    """Base field."""

    def __init__(self):
        self.value = None

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


class DateTimeField(BaseField):
    """Date and time field."""
