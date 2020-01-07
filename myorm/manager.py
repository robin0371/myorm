"""myorm manager module."""
from myorm.fields import IntegerField
from myorm.backend import OPS_MAP
from myorm.db import DATABASES


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
        columns = [name for name in instance.fields_names if name != "id"]
        values = [getattr(instance, name) for name in columns]

        insert_query = self.ops.get_query(
            op_type, table=instance.table, columns=columns
        )

        object_id = self.ops.execute(op_type, query=insert_query, values=values)

        id_field = IntegerField()
        id_field.value = object_id
        instance.id = id_field

        return instance

    def query_set(self, cols, rows):
        query_set = []
        model = type(self.model)

        for row in rows:
            params = {}
            for field_name, value in zip(cols, row):
                field = getattr(model, field_name)
                if hasattr(field, "to_python"):
                    value = type(field)(value).to_python()
                params[field_name] = value

            instance = model(**params)
            query_set.append(instance)

        return query_set

    def all(self):
        """Return all rows."""
        op_type = "read"

        fields = self.model.get_fields()

        select_query = self.ops.get_query(
            op_type, table=self.model.table, columns=fields["columns"]
        )

        rows = self.ops.execute(op_type, query=select_query)

        return self.query_set(fields["columns"], rows)

    def delete(self, instance):
        """Delete object."""
        op_type = "delete"

        delete_query = self.ops.get_query(op_type, table=self.model.table)

        self.ops.execute(op_type, query=delete_query, pk=instance.pk)

        instance.pk = None

    def update(self, instance):
        """Update object."""
        op_type = "update"

        columns = [name for name in instance.fields_names if name != "id"]
        values = [getattr(instance, name) for name in columns]

        update_query = self.ops.get_query(
            op_type, table=instance.table, columns=columns
        )

        self.ops.execute(op_type, query=update_query, values=values, pk=instance.pk)
