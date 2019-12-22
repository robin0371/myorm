"""myorm database connections module."""
import os

from myorm.util import get_project_root

# Not located in settings for simplicity
DATABASES = {
    "postgres": {
        "host": "localhost",
        "port": 54320,
        "user": "myorm_user",
        "password": "myorm_user",
        "database": "myorm_db",
    },
    "mysql": {
        "host": "localhost",
        "user": "myorm_user",
        "password": "myorm_user",
        "database": "myorm_db",
    },
    "sqlite": {"db": os.path.join(get_project_root(), "db", "sqlite.db"),},
}
