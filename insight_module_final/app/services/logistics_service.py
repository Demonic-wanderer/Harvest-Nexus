import json
import os
from typing import Optional

try:
    from shared.forge_client import ForgeClientError, submit_logistics
    from shared.geo import geocode_location, haversine_km
except ImportError:
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
    from shared.forge_client import ForgeClientError, submit_logistics
    from shared.geo import geocode_location, haversine_km

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "transporters.json")
DEFAULT_RATE_PER_KM_QUINTAL = 2.5


def load_transporters() -> list[dict]:
    path = os.path.abspath(DATA_FILE)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def estimate_transport_cost(distance_km: float, quantity_quintals: float, rate: float = DEFAULT_RATE_PER_KM_QUINTAL) -> float:
    if distance_km <= 0 or quantity_quintals <= 0:
        return 0.0
    return round(distance_km * quantity_quintals * rate, 2)


def is_worth_transporting(local_price: float, remote_price: float, transport_cost: float,
                           quantity_quintals: float) -> bool:
    price_gain = (remote_price - local_price) * quantity_quintals
    return price_gain > transport_cost


def _resolve(lat: Optional[float], lon: Optional[float], location: Optional[str]):
    if lat is not None and lon is not None:
        return lat, lon
    return geocode_location(location)


def quote_route(
    quantity_quintals: float,
    origin_lat: Optional[float] = None,
    origin_lon: Optional[float] = None,
    dest_lat: Optional[float] = None,
    dest_lon: Optional[float] = None,
    origin: Optional[str] = None,
    destination: Optional[str] = None,
) -> dict:
    start = _resolve(origin_lat, origin_lon, origin)
    end = _resolve(dest_lat, dest_lon, destination)
    if not start or not end:
        raise ValueError("Need coordinates or a known city name for origin and destination")

    distance_km = haversine_km(start[0], start[1], end[0], end[1])
    quotes = []
    for transporter in load_transporters():
        if quantity_quintals > float(transporter.get("capacity_quintals") or 0):
            continue
        rate = float(transporter.get("rate_per_km_quintal") or DEFAULT_RATE_PER_KM_QUINTAL)
        cost = estimate_transport_cost(distance_km, quantity_quintals, rate)
        quotes.append({
            "transporter_name": transporter["name"],
            "contact_phone": transporter.get("contact_phone"),
            "vehicle_type": transporter.get("vehicle_type"),
            "capacity_quintals": transporter.get("capacity_quintals"),
            "estimated_cost": cost,
            "rate_per_km_quintal": rate,
        })
    quotes.sort(key=lambda item: item["estimated_cost"])
    return {
        "distance_km": distance_km,
        "origin": {"lat": start[0], "lon": start[1], "label": origin},
        "destination": {"lat": end[0], "lon": end[1], "label": destination},
        "quotes": quotes,
    }


def book_transport(transaction_id: str, quote: dict, pickup_location: str, drop_location: str, persist: bool = True) -> dict:
    booking = {
        "transaction_id": transaction_id,
        "transporter_name": quote.get("transporter_name"),
        "contact_phone": quote.get("contact_phone"),
        "pickup_location": pickup_location,
        "drop_location": drop_location,
        "estimated_cost": quote.get("estimated_cost"),
        "status": "arranged",
    }
    if persist:
        try:
            booking["forge"] = submit_logistics({
                "transaction_id": transaction_id,
                "transporter_name": quote.get("transporter_name"),
                "contact_phone": quote.get("contact_phone"),
                "pickup_location": pickup_location,
                "drop_location": drop_location,
            })
            booking["forge_persisted"] = True
        except ForgeClientError as exc:
            booking["forge_persisted"] = False
            booking["forge_error"] = str(exc)
    return booking
