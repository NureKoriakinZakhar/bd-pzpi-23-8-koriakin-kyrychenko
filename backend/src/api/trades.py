from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.schemas.models import CryptoOut, TradeCreate, TradeOut
from src.core.security import get_current_user_data
from src.db.database import get_db_conn
import pyodbc

router = APIRouter(prefix="/api", tags=["Trading"])

@router.get("/cryptos", response_model=List[CryptoOut])
def get_cryptos(conn: pyodbc.Connection = Depends(get_db_conn)):
    cursor = conn.cursor()
    cursor.execute("SELECT crypto_id, name, symbol, price_usd FROM Cryptos")
    
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return results

@router.post("/trades")
def create_trade(trade: TradeCreate,user_data: dict = Depends(get_current_user_data),conn: pyodbc.Connection = Depends(get_db_conn)):
    cursor = conn.cursor()
    try:
        # Отримуємо wallet_id автоматично з токена
        wallet_id = user_data["wallet_id"]
        
        # Виклик процедури
        sql = "{CALL AddTrade (?, ?, ?, ?)}"
        params = (wallet_id, trade.crypto_id, trade.quantity, trade.trade_type)
        
        cursor.execute(sql, params)
        conn.commit()
        return {"message": "Trade executed", "by_user": user_data["username"]}

    except pyodbc.Error as e:
        conn.rollback()
        msg = str(e)
        if '50001' in msg: raise HTTPException(400, "Кількість має бути > 0")
        if '50002' in msg: raise HTTPException(400, "Невірний тип угоди")
        if '50003' in msg: raise HTTPException(404, "Гаманець не знайдено")
        if '50004' in msg: raise HTTPException(404, "Криптовалюту не знайдено")
        raise HTTPException(500, f"Помилка БД: {msg}")

@router.get("/my-trades", response_model=List[TradeOut])
def get_my_trades(user_data: dict = Depends(get_current_user_data), conn: pyodbc.Connection = Depends(get_db_conn)):
    cursor = conn.cursor()
    wallet_id = user_data["wallet_id"]
    
    # Виклик табличної функції
    cursor.execute("SELECT * FROM dbo.GetWalletTrades(?)", (wallet_id,))
    
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return results

@router.get("/my-count")
def get_trade_count(user_data: dict = Depends(get_current_user_data), conn: pyodbc.Connection = Depends(get_db_conn)):
    cursor = conn.cursor()
    wallet_id = user_data["wallet_id"]
    
    # Виклик скалярної функції
    cursor.execute("SELECT dbo.CountWalletTrades(?)", (wallet_id,))
    count = cursor.fetchval()
    
    return {"wallet_id": wallet_id, "total_trades": count}