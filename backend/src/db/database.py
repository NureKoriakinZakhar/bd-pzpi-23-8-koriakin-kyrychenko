import pyodbc
from src.core.config import settings

def get_db_conn():
    """
    Відкриває з'єднання, передає його в функцію, 
    а після завершення запиту автоматично закриває.
    """
    conn = pyodbc.connect(settings.DATABASE_CONN_STR)
    try:
        yield conn
    finally:
        conn.close()