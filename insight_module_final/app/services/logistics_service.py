TRANSPORT_RATE_PER_KM = 2.5


def estimate_transport_cost(distance_km: float, quantity_quintals: float) -> float:
    if distance_km <= 0 or quantity_quintals <= 0:
        return 0.0
    return round(distance_km * quantity_quintals * TRANSPORT_RATE_PER_KM, 2)


def is_worth_transporting(local_price: float, remote_price: float, transport_cost: float,
                           quantity_quintals: float) -> bool:
    price_gain = (remote_price - local_price) * quantity_quintals
    return price_gain > transport_cost
