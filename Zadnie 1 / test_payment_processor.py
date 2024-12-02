import unittest
from unittest.mock import Mock, patch
from payment_processor import (
    PaymentProcessor,
    PaymentGateway,
    TransactionResult,
    TransactionStatus,
    NetworkException,
    PaymentException,
    RefundException,
    dziennik
)

class TestPaymentProcessor(unittest.TestCase):

    def setUp(self):
        self.paymentGateway = Mock(spec=PaymentGateway)
        self.paymentProcessor = PaymentProcessor(self.paymentGateway)

    # Testy dla processPayment

    def test_processPayment_success(self):
        # Mockowanie odpowiedzi PaymentGateway
        self.paymentGateway.charge.return_value = TransactionResult(
            success=True,
            transactionId='tx123'
        )
        wynik = self.paymentProcessor.processPayment('user123', 100.0)
        self.assertTrue(wynik.success)
        self.assertEqual(wynik.transactionId, 'tx123')
        self.paymentGateway.charge.assert_called_once_with('user123', 100.0)

    def test_processPayment_failure_insufficient_funds(self):
        self.paymentGateway.charge.return_value = TransactionResult(
            success=False,
            transactionId='',
            message='Insufficient funds'
        )
        wynik = self.paymentProcessor.processPayment('user123', 100.0)
        self.assertFalse(wynik.success)
        self.assertEqual(wynik.message, 'Insufficient funds')
        self.paymentGateway.charge.assert_called_once_with('user123', 100.0)

    def test_processPayment_NetworkException(self):
        self.paymentGateway.charge.side_effect = NetworkException('Błąd sieci')
        wynik = self.paymentProcessor.processPayment('user123', 100.0)
        self.assertFalse(wynik.success)
        self.assertEqual(wynik.message, 'Błąd sieci')
        self.paymentGateway.charge.assert_called_once_with('user123', 100.0)

    def test_processPayment_PaymentException(self):
        self.paymentGateway.charge.side_effect = PaymentException('Błąd płatności')
        wynik = self.paymentProcessor.processPayment('user123', 100.0)
        self.assertFalse(wynik.success)
        self.assertEqual(wynik.message, 'Błąd płatności')
        self.paymentGateway.charge.assert_called_once_with('user123', 100.0)

    def test_processPayment_invalid_amount(self):
        with self.assertRaises(ValueError) as kontekst:
            self.paymentProcessor.processPayment('user123', -50.0)
        self.assertEqual(str(kontekst.exception), 'Kwota musi być dodatnia')

    def test_processPayment_empty_userId(self):
        with self.assertRaises(ValueError) as kontekst:
            self.paymentProcessor.processPayment('', 100.0)
        self.assertEqual(str(kontekst.exception), 'Identyfikator użytkownika nie może być pusty')

    # Testy dla refundPayment

    def test_refundPayment_success(self):
        self.paymentGateway.refund.return_value = TransactionResult(
            success=True,
            transactionId='tx123'
        )
        wynik = self.paymentProcessor.refundPayment('tx123')
        self.assertTrue(wynik.success)
        self.assertEqual(wynik.transactionId, 'tx123')
        self.paymentGateway.refund.assert_called_once_with('tx123')

    def test_refundPayment_failure_nonexistent_transaction(self):
        self.paymentGateway.refund.return_value = TransactionResult(
            success=False,
            transactionId='tx123',
            message='Transaction not found'
        )
        wynik = self.paymentProcessor.refundPayment('tx123')
        self.assertFalse(wynik.success)
        self.assertEqual(wynik.message, 'Transaction not found')
        self.paymentGateway.refund.assert_called_once_with('tx123')

    def test_refundPayment_NetworkException(self):
        self.paymentGateway.refund.side_effect = NetworkException('Błąd sieci')
        wynik = self.paymentProcessor.refundPayment('tx123')
        self.assertFalse(wynik.success)
        self.assertEqual(wynik.message, 'Błąd sieci')
        self.paymentGateway.refund.assert_called_once_with('tx123')

    def test_refundPayment_RefundException(self):
        self.paymentGateway.refund.side_effect = RefundException('Błąd zwrotu')
        wynik = self.paymentProcessor.refundPayment('tx123')
        self.assertFalse(wynik.success)
        self.assertEqual(wynik.message, 'Błąd zwrotu')
        self.paymentGateway.refund.assert_called_once_with('tx123')

    def test_refundPayment_empty_transactionId(self):
        with self.assertRaises(ValueError) as kontekst:
            self.paymentProcessor.refundPayment('')
        self.assertEqual(str(kontekst.exception), 'Identyfikator transakcji nie może być pusty')

    # Testy dla getPaymentStatus

    def test_getPaymentStatus_success(self):
        self.paymentGateway.getStatus.return_value = TransactionStatus.COMPLETED
        status = self.paymentProcessor.getPaymentStatus('tx123')
        self.assertEqual(status, TransactionStatus.COMPLETED)
        self.paymentGateway.getStatus.assert_called_once_with('tx123')

    def test_getPaymentStatus_nonexistent_transaction(self):
        self.paymentGateway.getStatus.return_value = TransactionStatus.FAILED
        status = self.paymentProcessor.getPaymentStatus('tx999')
        self.assertEqual(status, TransactionStatus.FAILED)
        self.paymentGateway.getStatus.assert_called_once_with('tx999')

    def test_getPaymentStatus_NetworkException(self):
        self.paymentGateway.getStatus.side_effect = NetworkException('Błąd sieci')
        status = self.paymentProcessor.getPaymentStatus('tx123')
        self.assertEqual(status, TransactionStatus.FAILED)
        self.paymentGateway.getStatus.assert_called_once_with('tx123')

    def test_getPaymentStatus_empty_transactionId(self):
        with self.assertRaises(ValueError) as kontekst:
            self.paymentProcessor.getPaymentStatus('')
        self.assertEqual(str(kontekst.exception), 'Identyfikator transakcji nie może być pusty')

    # Testy logowania i użycia spy

    @patch('payment_processor.dziennik')
    def test_processPayment_logs_success(self, mock_dziennik):
        self.paymentGateway.charge.return_value = TransactionResult(
            success=True,
            transactionId='tx123'
        )
        self.paymentProcessor.processPayment('user123', 100.0)
        mock_dziennik.info.assert_called_with('Płatność udana dla użytkownika user123')

    @patch('payment_processor.dziennik')
    def test_processPayment_logs_failure(self, mock_dziennik):
        self.paymentGateway.charge.return_value = TransactionResult(
            success=False,
            transactionId='',
            message='Insufficient funds'
        )
        self.paymentProcessor.processPayment('user123', 100.0)
        mock_dziennik.error.assert_called_with('Płatność nieudana dla użytkownika user123: Insufficient funds')

    @patch('payment_processor.dziennik')
    def test_processPayment_logs_exception(self, mock_dziennik):
        self.paymentGateway.charge.side_effect = PaymentException('Błąd płatności')
        self.paymentProcessor.processPayment('user123', 100.0)
        mock_dziennik.error.assert_called_with('Błąd podczas przetwarzania płatności dla użytkownika user123: Błąd płatności')

    @patch('payment_processor.dziennik')
    def test_refundPayment_logs_success(self, mock_dziennik):
        self.paymentGateway.refund.return_value = TransactionResult(
            success=True,
            transactionId='tx123'
        )
        self.paymentProcessor.refundPayment('tx123')
        mock_dziennik.info.assert_called_with('Zwrot udany dla transakcji tx123')

    @patch('payment_processor.dziennik')
    def test_refundPayment_logs_failure(self, mock_dziennik):
        self.paymentGateway.refund.return_value = TransactionResult(
            success=False,
            transactionId='tx123',
            message='Transaction not found'
        )
        self.paymentProcessor.refundPayment('tx123')
        mock_dziennik.error.assert_called_with('Zwrot nieudany dla transakcji tx123: Transaction not found')

    @patch('payment_processor.dziennik')
    def test_getPaymentStatus_logs(self, mock_dziennik):
        self.paymentGateway.getStatus.return_value = TransactionStatus.COMPLETED
        self.paymentProcessor.getPaymentStatus('tx123')
        mock_dziennik.info.assert_called_with('Status transakcji tx123: COMPLETED')

    @patch('payment_processor.dziennik')
    def test_getPaymentStatus_logs_exception(self, mock_dziennik):
        self.paymentGateway.getStatus.side_effect = NetworkException('Błąd sieci')
        self.paymentProcessor.getPaymentStatus('tx123')
        mock_dziennik.error.assert_called_with('Błąd podczas pobierania statusu transakcji tx123: Błąd sieci')

if __name__ == '__main__':
    unittest.main()