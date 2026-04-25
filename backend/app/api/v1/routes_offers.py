from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.offer import Offer
from app.models.price_history import PriceHistory
from app.schemas.offer import OfferCreate, OfferPriceUpdate, OfferResponse
from app.schemas.price_history import PriceHistoryResponse
from app.services.price_analysis import detect_fake_discount


router = APIRouter(prefix="/offers", tags=["offers"])


def build_offer_response(offer: Offer, db: Session) -> OfferResponse:
    history = (
        db.query(PriceHistory)
        .filter(PriceHistory.offer_id == offer.id)
        .order_by(PriceHistory.recorded_at.desc())
        .limit(5)
        .all()
    )
    discount_type, confidence_score = detect_fake_discount(offer, history)
    return OfferResponse.model_validate(offer).model_copy(
        update={
            "discount_type": discount_type,
            "confidence_score": confidence_score,
        }
    )


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
def list_offers(db: Session = Depends(get_db)) -> list[OfferResponse]:
    offers = db.query(Offer).all()
    return [build_offer_response(offer, db) for offer in offers]


@router.get("/fake", response_model=list[OfferResponse])
def list_fake_offers(db: Session = Depends(get_db)) -> list[OfferResponse]:
    offers = db.query(Offer).all()
    fake_offers: list[OfferResponse] = []

    for offer in offers:
        offer_response = build_offer_response(offer, db)
        if offer_response.discount_type == "fake":
            fake_offers.append(offer_response)

    return fake_offers


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


@router.patch("/{offer_id}/price", response_model=OfferResponse)
def update_offer_price(
    offer_id: int, payload: OfferPriceUpdate, db: Session = Depends(get_db)
) -> OfferResponse:
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")

    if offer.current_price == payload.current_price:
        return build_offer_response(offer, db)

    offer.current_price = payload.current_price
    offer.updated_at = datetime.utcnow()

    db.add(
        PriceHistory(
            offer_id=offer.id,
            price=payload.current_price,
        )
    )

    db.commit()
    db.refresh(offer)
    return build_offer_response(offer, db)
