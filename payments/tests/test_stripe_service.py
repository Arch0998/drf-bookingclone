from unittest.mock import patch, MagicMock

import stripe
from django.test import TestCase


def create_checkout_session(amount, currency, success_url, cancel_url):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": currency,
                    "product_data": {"name": "Test Product"},
                    "unit_amount": amount,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


def retrieve_checkout_session(session_id):
    return stripe.checkout.Session.retrieve(session_id)


class StripeServiceMockTest(TestCase):
    @patch("stripe.checkout.Session.create")
    def test_create_checkout_session(self, mock_create):
        mock_session = MagicMock()
        mock_session.id = "sess_123"
        mock_session.url = "https://stripe.com/pay/sess_123"
        mock_create.return_value = mock_session
        
        session = create_checkout_session(
            amount=1000,
            currency="usd",
            success_url="https://test/success",
            cancel_url="https://test/cancel",
        )
        self.assertEqual(session.id, "sess_123")
        self.assertEqual(session.url, "https://stripe.com/pay/sess_123")
        mock_create.assert_called_once()
    
    @patch("stripe.checkout.Session.retrieve")
    def test_retrieve_checkout_session(self, mock_retrieve):
        mock_session = MagicMock()
        mock_session.payment_status = "paid"
        mock_retrieve.return_value = mock_session
        
        session = retrieve_checkout_session("sess_123")
        self.assertEqual(session.payment_status, "paid")
        mock_retrieve.assert_called_once_with("sess_123")
