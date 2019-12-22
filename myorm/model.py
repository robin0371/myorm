"""myorm model module."""
from inflection import pluralize

from myorm.fields import BaseField
from myorm.manager import Manager


class BaseModel:
    """Base class for custom models."""

    def __new__(cls, *args, **kwargs):
        model = super(BaseModel, cls).__new__(cls)

        cls.add_to_class(model, "objects", Manager())

        return model

    def __init__(self, *args, **kwargs):
        for name, value in kwargs.items():
            field = getattr(self, name)
            field.value = value

    def add_to_class(self, name, obj):
        setattr(self, name, obj)
        obj.set_model(self)

    @property
    def table(self):
        """Return table name."""
        return pluralize(self.__class__.__name__).lower()

    @property
    def id(self):
        id_field = getattr(self, "id")
        return id_field.value

    @id.setter
    def id(self, object_id):
        id_field = getattr(self, "id")
        id_field.value = object_id

    def get_fields(self, exclude=None) -> dict:
        """Return model fields."""
        fields = {"values": [], "columns": []}
        if exclude is None:
            exclude = []

        for name in dir(self):
            if name in exclude:
                continue

            if isinstance(getattr(self, name), BaseField):
                field = getattr(self, name)
                fields["values"].append(field.value)
                fields["columns"].append(name)

        return fields

    def save(self):
        """Save instance into database."""
        if self.id is None:
            self.objects.create(self)

    def all(self):
        return self.objects.all()
