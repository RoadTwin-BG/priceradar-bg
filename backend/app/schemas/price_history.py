from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PriceHistoryResponse(BaseModel):
    id: int
    offer_id: int
    price: Decimal = Field(gt=0)
    recorded_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "offer_id": 1,
                "price": "799.99",
                "recorded_at": "2026-04-25T08:37:29",
            }
        },
    )
