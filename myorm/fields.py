"""myorm fields module."""
import datetime


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

    def to_python(self) -> bool:
        return bool(self.value)


class DateField(BaseField):
    """Date field."""

    def to_python(self):
        if not isinstance(self.value, datetime.date):
            return datetime.date.fromisoformat(self.value)
        return self.value
