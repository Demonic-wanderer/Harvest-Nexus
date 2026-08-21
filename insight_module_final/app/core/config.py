"""
Config for the Insight (Market Intelligence & Buyer Linkage) module.
Currently the working CLI tool uses its own sqlite connection directly
in db/database.py — these settings are for the API/service layer below,
which you can wire up when you're ready to expose HTTP endpoints.
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Harvest Nexus - Insight Module"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./insight_module.db"
    )
    MARKET_PRICE_API_KEY: str = os.getenv("MARKET_PRICE_API_KEY", "")
    GOV_AGRI_DATA_API_URL: str = os.getenv(
        "GOV_AGRI_DATA_API_URL", "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a24601d3dead"
    )
    RISING_TREND_THRESHOLD_PCT: float = 3.0
    FALLING_TREND_THRESHOLD_PCT: float = -3.0


settings = Settings()
