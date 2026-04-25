from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class OfferCreate(BaseModel):
    product_id: int
    store_id: int
    product_url: str
    current_price: Decimal = Field(gt=0)
    original_price: Decimal | None = Field(default=None, gt=0)
    currency: Literal["EUR", "BGN"] = "EUR"
    is_active: bool = True

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "product_id": 1,
                "store_id": 1,
                "product_url": "https://example.com/product",
                "current_price": "1299.99",
                "original_price": "1499.99",
                "currency": "EUR",
                "is_active": True,
            }
        }
    )


class OfferPriceUpdate(BaseModel):
    current_price: Decimal = Field(gt=0)


class OfferResponse(BaseModel):
    id: int
    product_id: int
    store_id: int
    product_url: str
    current_price: Decimal = Field(gt=0)
    original_price: Decimal | None = Field(default=None, gt=0)
    currency: Literal["EUR", "BGN"] = "EUR"
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "product_id": 1,
                "store_id": 1,
                "product_url": "https://example.com/product",
                "current_price": "1299.99",
                "original_price": "1499.99",
                "currency": "EUR",
                "is_active": True,
                "created_at": "2026-04-25T08:00:00",
                "updated_at": "2026-04-25T08:00:00",
            }
        },
    )
