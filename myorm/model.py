"""myorm model module."""
from inflection import pluralize

from myorm.fields import BaseField
from myorm.manager import Manager


class BaseModel:
    """Base class for custom models."""

    def __new__(cls, *args, **kwargs):
        model = super(BaseModel, cls).__new__(cls)
        model.pk = None

        fields = model.get_fields()
        model.fields_names = fields["columns"]

        cls.add_to_class(model, "objects", Manager())

        return model

    def __init__(self, *args, **kwargs):
        fields = self.get_fields()
        for name, value in kwargs.items():
            if name in fields["columns"]:
                field = getattr(self, name)
                field.value = value
                setattr(self, name, value)

    def add_to_class(self, name, obj) -> None:
        setattr(self, name, obj)
        obj.set_model(self)

    @property
    def table(self) -> str:
        """Return table name."""
        return pluralize(self.__class__.__name__).lower()

    @property
    def pk(self):
        id_field = getattr(self, "id")
        if isinstance(id_field, BaseField):
            return id_field.value
        return id_field

    @pk.setter
    def pk(self, object_id):
        id_field = getattr(self, "id")
        id_field.value = object_id

    def get_fields(self) -> dict:
        """Return model fields."""
        fields: dict = {"values": [], "columns": []}

        for name in dir(self):
            if isinstance(getattr(self, name), BaseField):
                field = getattr(self, name)
                fields["values"].append(field.value)
                fields["columns"].append(name)

        return fields

    def save(self):
        """Save object."""
        if self.pk is None:
            self.objects.create(self)
        else:
            self.objects.update(self)

    def all(self):
        """Return all objects."""
        return self.objects.all()

    def first(self):
        """Return first object."""
        objects = self.all()
        return objects[0] if objects else None

    def last(self):
        """Return last object."""
        objects = self.all()
        return objects[-1] if objects else None

    def delete(self):
        """Delete object."""
        self.objects.delete(self)
