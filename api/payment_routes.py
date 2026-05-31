from fastapi import APIRouter
from fastapi import Header

from app.model.model_payment import PaymentRequest

from app.use_cases.process_payment import ProcessPaymentUseCase

from domain.entities.payment import Payment

from infra.redis.redis_client import redis_client

from infra.repositories.memory_payment_repository import MemoryPaymentRepository

router = APIRouter()

repository = MemoryPaymentRepository()

use_case = ProcessPaymentUseCase(repository=repository, redis_client=redis_client)


@router.post("/payments")
def process_payment(request: PaymentRequest, idempotency_key: str = Header(...)):

    payment = Payment(user_id=request.user_id, amount=request.amount)

    return use_case.execute(payment=payment, idempotency_key=idempotency_key)