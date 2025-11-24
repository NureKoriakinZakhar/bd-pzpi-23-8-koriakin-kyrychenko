from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
# ЗМІНА: Використовуємо HTTPBearer замість OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials 
from jose import JWTError, jwt
from src.core.config import settings
from src.db.database import get_db_conn
import pyodbc

# Це зробить просте поле "Value" у Swagger
security_scheme = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def get_current_user_data(
    # ЗМІНА: Отримуємо токен через HTTPBearer
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme), 
    conn: pyodbc.Connection = Depends(get_db_conn)
) -> dict:
    token = credentials.credentials # Дістаємо сам рядок токена
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        user_id = int(user_id_str)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    cursor = conn.cursor()
    query = """
        SELECT u.user_id, u.username, w.wallet_id
        FROM Users u
        JOIN Wallets w ON u.user_id = w.user_id
        WHERE u.user_id = ?
    """
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()

    if not row:
        raise HTTPException(status_code=401, detail="User or Wallet not found")

    return {
        "user_id": row.user_id,
        "username": row.username,
        "wallet_id": row.wallet_id
    }