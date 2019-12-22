"""myorm utils module."""
import os


def get_project_root():
    """Return path to project root."""
    return os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
