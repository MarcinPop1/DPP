from abc import ABC, abstractmethod
from enum import Enum
import logging

# Konfiguracja logowania
dziennik = logging.getLogger(__name__)
dziennik.setLevel(logging.INFO)
uchwyt = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
uchwyt.setFormatter(formatter)
dziennik.addHandler(uchwyt)

# Enum TransactionStatus z wartościami z treści zadania
class TransactionStatus(Enum):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

# Klasa TransactionResult z polami z treści zadania
class TransactionResult:
    def __init__(self, success: bool, transactionId: str, message: str = ''):
        self.success = success
        self.transactionId = transactionId
        self.message = message

# Wyjątki z treści zadania
class NetworkException(Exception):
    pass

class PaymentException(Exception):
    pass

class RefundException(Exception):
    pass

# Interfejs PaymentGateway z metodami z treści zadania
class PaymentGateway(ABC):

    @abstractmethod
    def charge(self, userId: str, amount: float) -> TransactionResult:
        pass

    @abstractmethod
    def refund(self, transactionId: str) -> TransactionResult:
        pass

    @abstractmethod
    def getStatus(self, transactionId: str) -> TransactionStatus:
        pass

# Implementacja klasy PaymentProcessor z metodami z treści zadania
class PaymentProcessor:

    def __init__(self, paymentGateway: PaymentGateway):
        self.paymentGateway = paymentGateway

    def processPayment(self, userId: str, amount: float) -> TransactionResult:
        # Walidacja danych wejściowych
        if not userId:
            raise ValueError('Identyfikator użytkownika nie może być pusty')
        if amount <= 0:
            raise ValueError('Kwota musi być dodatnia')

        try:
            wynik = self.paymentGateway.charge(userId, amount)
            if wynik.success:
                dziennik.info(f'Płatność udana dla użytkownika {userId}')
            else:
                dziennik.error(f'Płatność nieudana dla użytkownika {userId}: {wynik.message}')
            return wynik
        except (NetworkException, PaymentException) as e:
            dziennik.error(f'Błąd podczas przetwarzania płatności dla użytkownika {userId}: {str(e)}')
            return TransactionResult(success=False, transactionId='', message=str(e))

    def refundPayment(self, transactionId: str) -> TransactionResult:
        # Walidacja danych wejściowych
        if not transactionId:
            raise ValueError('Identyfikator transakcji nie może być pusty')

        try:
            wynik = self.paymentGateway.refund(transactionId)
            if wynik.success:
                dziennik.info(f'Zwrot udany dla transakcji {transactionId}')
            else:
                dziennik.error(f'Zwrot nieudany dla transakcji {transactionId}: {wynik.message}')
            return wynik
        except (NetworkException, RefundException) as e:
            dziennik.error(f'Błąd podczas przetwarzania zwrotu dla transakcji {transactionId}: {str(e)}')
            return TransactionResult(success=False, transactionId=transactionId, message=str(e))

    def getPaymentStatus(self, transactionId: str) -> TransactionStatus:
        # Walidacja danych wejściowych
        if not transactionId:
            raise ValueError('Identyfikator transakcji nie może być pusty')

        try:
            status = self.paymentGateway.getStatus(transactionId)
            dziennik.info(f'Status transakcji {transactionId}: {status.value}')
            return status
        except NetworkException as e:
            dziennik.error(f'Błąd podczas pobierania statusu transakcji {transactionId}: {str(e)}')
            return TransactionStatus.FAILED