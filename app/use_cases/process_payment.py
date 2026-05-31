import json
import time
from fastapi import HTTPException

from domain.entities.payment import Payment
from app.utils.hash_generator import generate_request_hash


# Regra de Negócio
class ProcessPaymentUseCase:

    def __init__(self, repository, redis_client):
        self.repository = repository
        self.redis_client = redis_client

    def execute(self, payment: Payment, idempotency_key: str):

        # Chave Redis
        cache_key = f"idempotency:{idempotency_key}"

        request_payload = {
            "user_id": payment.user_id,
            "amount": payment.amount
        }

        # Hash da Requisição
        request_hash = generate_request_hash(
            request_payload
        )

        # Verificar Chave no Redis
        cached = self.redis_client.get(
            cache_key
        )

        if cached:

            if cached == "PROCESSING":
                return {
                    "message": (
                        "payment already being processed"
                    )
                }

            cached_data = json.loads(cached)

            cached_response = cached_data["response"].copy()

            cached_response["source"] = "redis"

            if cached_data["request_hash"] != request_hash:
                raise HTTPException(
                    status_code=409,
                    detail=(
                        "Idempotency key already used "
                        "with different payload"
                    )
                )

            return cached_response

        # Lock Redis
        lock_created = self.redis_client.set(
            cache_key,
            "PROCESSING",
            nx=True,
            ex=60
        )

        if not lock_created:
            return {
                "message": (
                    "payment already being processed"
                )
            }

        time.sleep(5)

        # Stripe / Mercado Pago / Adyen
        self.repository.save(payment)

        response = {
            "status": "approved",
            "user_id": payment.user_id,
            "amount": payment.amount,
            "source": "processor"
        }

        redis_payload = {
            "request_hash": request_hash,
            "response": response
        }

        # Exemplo:
        """
                {
                    "request_hash": "abc123",
                    "response": {
                    "status": "approved",
                    "user_id": "1",
                    "amount": 100
                    }
                }
        """
        self.redis_client.set(
            cache_key,
            json.dumps(redis_payload),
            ex=3600
        )

        return response