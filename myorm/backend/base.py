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


class OperationStatement:
    @staticmethod
    @abc.abstractmethod
    def statement():
        """Return operation statement."""


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


class BaseCreateOperations(BaseOperation, OperationStatement):
    """Base create operations."""

    @staticmethod
    def statement():
        return "INSERT INTO"


class BaseReadOperations(BaseOperation, OperationStatement):
    """Base read operations."""

    @staticmethod
    def statement():
        return "SELECT"


class BaseUpdateOperations(BaseOperation, OperationStatement):
    """Base update operations."""

    @staticmethod
    def statement():
        return "UPDATE"


class BaseDeleteOperations(BaseOperation, OperationStatement):
    """Base delete operations."""

    @staticmethod
    def statement():
        return "DELETE"
