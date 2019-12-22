"""myorm specific functions for databases."""
from myorm.backend.postgresql import Operations as PostgreSQLOperations
from myorm.backend.mysql import Operations as MySQOperations
from myorm.backend.sqlite import Operations as SQLiteOperations


OPS_MAP = {
    "postgres": PostgreSQLOperations,
    "mysql": MySQOperations,
    "sqlite": SQLiteOperations,
}


__all__ = ("OPS_MAP",)
