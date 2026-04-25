from decimal import Decimal


def detect_fake_discount(offer, price_history):
    if offer.original_price is None:
        return None

    if not price_history:
        return None

    recent_prices = [entry.price for entry in price_history]
    max_recent_price = max(recent_prices)

    if offer.original_price > max_recent_price * Decimal("1.20"):
        return "fake"

    return "real"
