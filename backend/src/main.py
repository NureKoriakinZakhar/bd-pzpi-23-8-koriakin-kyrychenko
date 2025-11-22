from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Імпорт
from src.api import auth, trades

app = FastAPI(title="Crypto SQL Project")

# --- НАЛАШТУВАННЯ CORS (Дозволяємо браузеру стукатись до нас) ---
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500", # Стандартний порт VS Code Live Server
    "*" # Для тестів дозволяємо всім (у продакшні так не роблять)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Дозволяє будь-який сайт
    allow_credentials=True,
    allow_methods=["*"], # Дозволяє GET, POST, і т.д.
    allow_headers=["*"], # Дозволяє Authorization хедер
)
# -------------------------------------------------------------

app.include_router(auth.router)
app.include_router(trades.router)

@app.get("/")
def root():
    return {"status": "System Operational"}