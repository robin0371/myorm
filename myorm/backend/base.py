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

    def __init__(self, params):
        self.params = params
        self.connection = None

        self.make_connection()

    @abc.abstractmethod
    def make_connection(self):
        """Return new connection."""


class BaseCreateOperations(BaseOperation):
    """Base create operations."""

    @staticmethod
    def insert():
        """Insert query."""
        return "INSERT INTO"
