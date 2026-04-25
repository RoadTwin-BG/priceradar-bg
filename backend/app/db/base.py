from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so SQLAlchemy metadata can discover all tables.
from app.models.offer import Offer  # noqa: E402,F401
from app.models.price_history import PriceHistory  # noqa: E402,F401
from app.models.product import Product  # noqa: E402,F401
from app.models.store import Store  # noqa: E402,F401
