from dataclasses import dataclass


@dataclass
class Payment:
    """
    Entidade de domínio.

    Representa um pagamento
    independente de FastAPI,
    Redis ou Banco de Dados.
    """

    user_id: str
    amount: float