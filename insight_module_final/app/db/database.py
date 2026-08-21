import sqlite3

DB_NAME = "insight_module.db"


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    print("DATABASE:", DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market TEXT NOT NULL,
            commodity TEXT NOT NULL,
            price REAL NOT NULL,
            date TEXT
        )
    """)

    cursor.execute("PRAGMA table_info(market_prices)")
    columns = [row[1] for row in cursor.fetchall()]

    if "date" not in columns:
        cursor.execute(
            "ALTER TABLE market_prices ADD COLUMN date TEXT"
        )

    conn.commit()
    conn.close()


def add_market_price(market, commodity, price, date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO market_prices (market, commodity, price, date)
        VALUES (?, ?, ?, ?)
        """,
        (market, commodity, price, date)
    )

    conn.commit()
    conn.close()


def get_market_prices():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT market, commodity, price, date FROM market_prices"
    )

    rows = cursor.fetchall()
    conn.close()

    return rows
