from fastapi import FastAPI

from app.api.v1.routes_offers import router as offers_router
from app.api.v1.routes_products import router as products_router
from app.db.base import Base, import_models
from app.db.session import engine

app = FastAPI(title="PriceRadar BG API")


import_models()
Base.metadata.create_all(bind=engine)

app.include_router(products_router, prefix="/api/v1")
app.include_router(offers_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
