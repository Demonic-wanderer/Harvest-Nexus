from datetime import datetime

from db.database import add_market_price, get_market_prices


def save_price(crop_type, region, price_per_quintal):
    recorded_at = datetime.utcnow().isoformat()
    add_market_price(crop_type, region, price_per_quintal, recorded_at)


def list_prices():
    return get_market_prices()
