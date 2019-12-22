"""myorm manager module."""
from myorm.backend import OPS_MAP
from myorm.db import DATABASES
from myorm.fields import BaseField


class Manager:
    """Database manager."""

    db = None
    ops = None
    model = None

    def set_model(self, model):
        self.model = model

    def using(self, db: str):
        """Select db connection."""
        self.db = db
        connection_params = DATABASES[db]
        self.ops = OPS_MAP[db](connection_params)
        return self.model

    def create(self, instance):
        """Insert instance into database."""
        op_type = "create"
        columns, values = [], []

        for name in dir(instance):
            if isinstance(getattr(instance, name), BaseField) and name != "id":
                field = getattr(instance, name)
                values.append(field.value)
                columns.append(name)

        insert_query = self.ops.get_query(
            op_type, table=instance.table, columns=columns
        )

        object_id = self.ops.execute(op_type, query=insert_query, values=values)

        instance.pk = object_id

        return instance
