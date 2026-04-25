from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.offer import Offer
from app.models.price_history import PriceHistory
from app.schemas.offer import OfferCreate, OfferResponse
from app.schemas.price_history import PriceHistoryResponse


router = APIRouter(prefix="/offers", tags=["offers"])


@router.post("", response_model=OfferResponse, status_code=status.HTTP_201_CREATED)
def create_offer(payload: OfferCreate, db: Session = Depends(get_db)) -> Offer:
    offer = Offer(
        product_id=payload.product_id,
        store_id=payload.store_id,
        product_url=payload.product_url,
        current_price=payload.current_price,
        original_price=payload.original_price,
        currency=payload.currency,
        is_active=payload.is_active,
    )
    db.add(offer)
    db.flush()

    price_history = PriceHistory(
        offer_id=offer.id,
        price=offer.current_price,
    )
    db.add(price_history)

    db.commit()
    db.refresh(offer)
    return offer


@router.get("", response_model=list[OfferResponse])
def list_offers(db: Session = Depends(get_db)) -> list[Offer]:
    return db.query(Offer).all()


@router.get("/{offer_id}/history", response_model=list[PriceHistoryResponse])
def get_offer_history(offer_id: int, db: Session = Depends(get_db)) -> list[PriceHistory]:
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")

    return (
        db.query(PriceHistory)
        .filter(PriceHistory.offer_id == offer_id)
        .order_by(PriceHistory.recorded_at.desc())
        .all()
    )
