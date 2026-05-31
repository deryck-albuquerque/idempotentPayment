from domain.entities.payment import Payment
from domain.repositories.payment_repository import PaymentRepository


class MemoryPaymentRepository(PaymentRepository):

    def __init__(self):
        # Lista simulando uma tabela
        self._payments = []

    def save(self, payment: Payment):
        # Salva na memória
        self._payments.append(payment)