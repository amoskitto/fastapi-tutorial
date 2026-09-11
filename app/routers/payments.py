from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import hmac
import hashlib
import json

from app import models, oauth2
from app.database import get_db
from app.config import settings
from paystackapi.paystack import Paystack

paystack = Paystack(secret_key=settings.paystack_secret_key)

router = APIRouter(prefix="/payments", tags=["Payments"])

PRO_AMOUNT_KOBO = 50000
PRO_CURRENCY = "NGN"


def fulfill_pro(db: Session, *, reference: str, amount: int, currency: str, user_id_from_metadata=None):
    if amount != PRO_AMOUNT_KOBO or currency != PRO_CURRENCY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unexpected payment amount or currency",
        )

    payment = db.query(models.Payment).filter(models.Payment.reference == reference).first()
    if payment is None:
        if user_id_from_metadata is None:
            raise HTTPException(status_code=400, detail="Unknown payment reference")
        payment = models.Payment(
            user_id=int(user_id_from_metadata),
            reference=reference,
            amount=amount,
            currency=currency,
            status="pending",
        )
        db.add(payment)
        db.flush()

    if payment.status == "success":
        return payment

    if payment.amount != amount or payment.currency != currency:
        raise HTTPException(status_code=400, detail="Payment mismatch")

    user = db.query(models.User).filter(models.User.id == payment.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.subscription_status = "PRO"
    payment.status = "success"
    payment.paid_at = datetime.utcnow()
    db.commit()
    db.refresh(payment)
    return payment


@router.post("/create-checkout-session")
def create_checkout_session(
    current_user: models.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    user_id = getattr(current_user, "id", None) or getattr(current_user, "user_id", None)
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    try:
        response = paystack.transaction.initialize(
            email=user.email,
            amount=PRO_AMOUNT_KOBO,
            callback_url=settings.paystack_callback_url,
            metadata={
                "user_id": str(user.id),
                "custom_fields": [
                    {
                        "display_name": "User ID",
                        "variable_name": "user_id",
                        "value": str(user.id),
                    }
                ],
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment initialization failed: {e}",
        )

    if not response.get("status"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.get("message", "Failed to create checkout session"),
        )

    data = response["data"]
    db.add(
        models.Payment(
            user_id=user.id,
            reference=data["reference"],
            amount=PRO_AMOUNT_KOBO,
            currency=PRO_CURRENCY,
            status="pending",
        )
    )
    db.commit()

    return {
        "checkout_url": data["authorization_url"],
        "reference": data["reference"],
    }

print("KEY STARTS WITH:", settings.paystack_secret_key[:8])
print("KEY LENGTH:", len(settings.paystack_secret_key))


@router.get("/callback")
def payment_callback(reference: str, db: Session = Depends(get_db)):
    try:
        response = paystack.transaction.verify(reference)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment verification failed: {e}",
        )

    if not (response.get("status") and response.get("data", {}).get("status") == "success"):
        payment = db.query(models.Payment).filter(models.Payment.reference == reference).first()
        if payment and payment.status != "success":
            payment.status = "failed"
            db.commit()
        return {"message": "Payment verification failed", "status": "failed"}

    data = response["data"]
    metadata = data.get("metadata") or {}
    fulfill_pro(
        db,
        reference=data["reference"],
        amount=int(data["amount"]),
        currency=data.get("currency", PRO_CURRENCY),
        user_id_from_metadata=metadata.get("user_id"),
    )
    return {"message": "Payment successful! You are now a PRO user.", "status": "success"}


@router.post("/webhook")
async def paystack_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    signature = request.headers.get("x-paystack-signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")

    expected = hmac.new(
        settings.paystack_secret_key.encode("utf-8"),
        payload,
        hashlib.sha512,
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        raise HTTPException(status_code=401, detail="Invalid signature")

    event = json.loads(payload)
    if event.get("event") != "charge.success":
        return {"status": "ignored"}

    data = event["data"]
    if data.get("status") != "success":
        return {"status": "ignored"}

    metadata = data.get("metadata") or {}
    try:
        fulfill_pro(
            db,
            reference=data["reference"],
            amount=int(data["amount"]),
            currency=data.get("currency", PRO_CURRENCY),
            user_id_from_metadata=metadata.get("user_id"),
        )
    except HTTPException:
        return {"status": "unprocessed"}

    return {"status": "success"}