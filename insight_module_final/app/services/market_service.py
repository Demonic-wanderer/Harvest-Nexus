from datetime import date

from db.database import add_market_price, get_market_prices


def save_price(market, commodity, price):
    today = date.today().isoformat()
    add_market_price(market, commodity, price, today)


def list_prices():
    return get_market_prices()
