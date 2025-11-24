import pyodbc
from src.core.config import settings

def get_db_conn():
    conn = pyodbc.connect(settings.DATABASE_CONN_STR)
    try:
        yield conn
    finally:
        conn.close()