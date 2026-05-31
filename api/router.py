from fastapi import APIRouter

from api.payment_routes import router as payment_router

router = APIRouter()

router.include_router(
    payment_router,
    tags=["Payments"]
)