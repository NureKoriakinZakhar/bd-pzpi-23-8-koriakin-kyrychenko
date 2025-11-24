from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class LoginRequest(BaseModel):
    user_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TradeCreate(BaseModel):
    crypto_id: int
    quantity: float
    trade_type: str

class CryptoOut(BaseModel):
    crypto_id: int
    name: str
    symbol: Optional[str]
    price_usd: float

class TradeOut(BaseModel):
    trade_id: int
    quantity: float
    trade_date: date
    trade_type: str
    crypto_id: int