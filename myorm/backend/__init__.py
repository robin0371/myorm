"""myorm specific functions for databases."""
from myorm.backend.postgresql import Operations as PostgreSQLOperations
from myorm.backend.sqlite import Operations as SQLiteOperations

# from myorm.backend.mysql import Operation
# from myorm.backend.sqlite import Operation


OPS_MAP = {
    "postgres": PostgreSQLOperations,
    "sqlite": SQLiteOperations,
}


__all__ = ("OPS_MAP",)
