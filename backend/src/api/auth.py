from fastapi import APIRouter, Depends, HTTPException
from src.schemas.models import LoginRequest, Token
from src.core.security import create_access_token
from src.db.database import get_db_conn
import pyodbc

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
def login(
    data: LoginRequest,
    conn: pyodbc.Connection = Depends(get_db_conn)
):
    cursor = conn.cursor()
    
    # Перевіряємо існування юзера
    cursor.execute("SELECT user_id FROM Users WHERE user_id = ?", (data.user_id,))
    user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=404, detail="User ID not found")
    
    # Створюємо токен
    access_token = create_access_token(data={"sub": str(data.user_id)})
    
    return {"access_token": access_token, "token_type": "bearer"}