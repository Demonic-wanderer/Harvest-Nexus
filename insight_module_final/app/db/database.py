import sqlite3

DB_NAME = "insight_module.db"


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    print("DATABASE:", DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_type TEXT NOT NULL,
            region TEXT NOT NULL,
            price_per_quintal REAL NOT NULL,
            recorded_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_market_price(crop_type, region, price_per_quintal, recorded_at):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO market_prices (crop_type, region, price_per_quintal, recorded_at)
        VALUES (?, ?, ?, ?)
        """,
        (crop_type, region, price_per_quintal, recorded_at)
    )

    conn.commit()
    conn.close()


def get_market_prices():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT crop_type, region, price_per_quintal, recorded_at FROM market_prices"
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


# SQLAlchemy configuration for FastAPI API layer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# If sqlite is in DATABASE_URL, create_engine options might differ, but standard create_engine works
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
