from abc import ABC, abstractmethod
from domain.entities.payment import Payment


class PaymentRepository(ABC):

    @abstractmethod
    def save(self, payment: Payment):
        """
        Salva um pagamento.

        Cada implementação decide
        onde armazenar os dados.
        """
        pass