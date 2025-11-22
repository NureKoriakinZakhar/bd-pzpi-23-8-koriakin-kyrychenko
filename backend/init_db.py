import pyodbc

# Твій рядок підключення
CONN_STR = "DRIVER={ODBC Driver 18 for SQL Server};SERVER=sql.bsite.net\MSSQL2016;DATABASE=kyrylokyrychenkonure_;UID=kyrylokyrychenkonure_;PWD=kyrylobest228;TrustServerCertificate=yes;"

def init_db():
    print("Підключаємось до БД...")
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()

    try:
        print("Створення процедури AddTrade...")
        # Видаляємо стару версію, якщо є
        cursor.execute("IF OBJECT_ID('AddTrade', 'P') IS NOT NULL DROP PROCEDURE AddTrade")
        # Створюємо нову
        cursor.execute("""
        CREATE PROCEDURE AddTrade
            @wallet_id INT,
            @crypto_id INT,
            @quantity FLOAT,
            @trade_type VARCHAR(10)
        AS
        BEGIN
            IF @quantity <= 0
                THROW 50001, 'Quantity must be > 0', 1;

            IF @trade_type NOT IN ('Buy','Sell')
                THROW 50002, 'Trade type must be Buy or Sell', 1;

            IF NOT EXISTS (SELECT 1 FROM Wallets WHERE wallet_id=@wallet_id)
                THROW 50003, 'Wallet does not exist', 1;

            IF NOT EXISTS (SELECT 1 FROM Cryptos WHERE crypto_id=@crypto_id)
                THROW 50004, 'Crypto does not exist', 1;

            INSERT INTO Trades(wallet_id, crypto_id, quantity, trade_type)
            VALUES (@wallet_id, @crypto_id, @quantity, @trade_type);
        END;
        """)

        print("Створення функції CountWalletTrades...")
        cursor.execute("IF OBJECT_ID('CountWalletTrades', 'FN') IS NOT NULL DROP FUNCTION CountWalletTrades")
        cursor.execute("""
        CREATE FUNCTION CountWalletTrades (@wallet_id INT)
        RETURNS INT
        AS
        BEGIN
            RETURN (
                SELECT COUNT(*)
                FROM Trades
                WHERE wallet_id = @wallet_id
            );
        END;
        """)

        print("Створення функції GetWalletTrades...")
        cursor.execute("IF OBJECT_ID('GetWalletTrades', 'IF') IS NOT NULL DROP FUNCTION GetWalletTrades")
        cursor.execute("""
        CREATE FUNCTION GetWalletTrades (@wallet_id INT)
        RETURNS TABLE
        AS
        RETURN (
            SELECT 
                trade_id,
                crypto_id,
                quantity,
                trade_date,
                trade_type
            FROM Trades
            WHERE wallet_id = @wallet_id
        );
        """)

        conn.commit()
        print("✅ Успішно! Всі функції та процедури створено.")

    except Exception as e:
        conn.rollback()
        print(f"❌ Помилка: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()