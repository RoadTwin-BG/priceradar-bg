from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    brand: str | None = None
    category: str | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str | None
    category: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
