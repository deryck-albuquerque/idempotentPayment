from pydantic import BaseModel


class PaymentRequest(BaseModel):
    """
    Body recebido pela API.
    """

    user_id: str
    amount: float


class PaymentResponse(BaseModel):
    """
    Resposta devolvida pela API.
    """

    status: str
    user_id: str
    amount: float