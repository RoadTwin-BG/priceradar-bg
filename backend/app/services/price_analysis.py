from decimal import Decimal
from typing import Literal


def detect_fake_discount(
    offer, price_history
) -> tuple[Literal["fake", "real"] | None, float | None]:
    if offer.original_price is None:
        return None, None

    if not price_history:
        return None, None

    recent_prices = [entry.price for entry in price_history[:5]]
    max_recent_price = max(recent_prices)
    if max_recent_price <= 0:
        return None, None

    if offer.original_price > max_recent_price * Decimal("1.20"):
        confidence = min(float((offer.original_price - max_recent_price) / max_recent_price), 1.0)
        return "fake", confidence

    confidence = 1.0 - min(
        float(abs(offer.original_price - max_recent_price) / max_recent_price), 1.0
    )
    return "real", confidence
