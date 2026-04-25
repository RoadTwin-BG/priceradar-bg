from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def import_models() -> None:
    # Import models so SQLAlchemy metadata can discover all tables.
    from app.models.offer import Offer  # noqa: F401
    from app.models.price_history import PriceHistory  # noqa: F401
    from app.models.product import Product  # noqa: F401
    from app.models.store import Store  # noqa: F401
