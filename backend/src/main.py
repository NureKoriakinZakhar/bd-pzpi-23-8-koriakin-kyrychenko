from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Імпорт
from src.api import auth, trades

app = FastAPI(title="Crypto SQL Project")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------------------------------

app.include_router(auth.router)
app.include_router(trades.router)

@app.get("/")
def root():
    return {"status": "System Operational"}