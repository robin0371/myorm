"""myorm base operations module."""
import abc


class BaseOperation:
    """Base operation."""

    @abc.abstractmethod
    def get_query(self, **kwargs):
        """Return SQL query."""

    @abc.abstractmethod
    def execute(self, *kwargs):
        """Execute query."""


class Operations(BaseOperation):
    """Database operations."""

    def get_query(self, op_type, **kwargs):
        operation = getattr(self, op_type)
        query = operation.get_query(**kwargs)
        return query

    def execute(self, op_type, **kwargs):
        operation = getattr(self, op_type)
        result = operation.execute(**kwargs)
        return result


class BaseCreateOperations(BaseOperation):
    """Base create operations."""

    @staticmethod
    def insert():
        """Insert query."""
        return "INSERT INTO"


class BaseReadOperations(BaseOperation):
    """Base read operations."""

    @staticmethod
    def select():
        """Select query."""
        return "SELECT"
