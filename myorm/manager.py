"""myorm manager module."""
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
        fields = self.model.get_fields(exclude=["id"])

        insert_query = self.ops.get_query(
            op_type, table=instance.table, columns=fields["columns"]
        )

        object_id = self.ops.execute(
            op_type, query=insert_query, values=fields["values"]
        )

        instance.id = object_id

        return instance

    def query_set(self, cols, rows):
        query_set = []
        model = type(self.model)

        for row in rows:
            params = {field_name: value for field_name, value in zip(cols, row)}
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
