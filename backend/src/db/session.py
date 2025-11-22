import pyodbc
from src.core.config import settings

def get_db_connection():
    return pyodbc.connect(settings.DB_CONNECTION)