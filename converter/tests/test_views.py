from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from converter.models import Currency


class ConvertCurrencyViewTest(APITestCase):
    def setUp(self):
        self.from_currency = Currency.objects.create(code="USD", name="Dollar", rate=Decimal("1.000000"))
        self.to_currency = Currency.objects.create(code="EUR", name="Euro", rate=Decimal("0.850000"))

    @patch("converter.services.convert_currency")
    def test_convert_currency_success(self, mock_convert_currency):
        mock_convert_currency.return_value = {
            "converted_amount": 85.0,
            "conversion_rate": 0.85,
        }
        response = self.client.post(
            reverse("convert-currency"),
            data={"from_currency": "USD", "to_currency": "EUR", "amount": 100},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"converted_amount": 85.0, "conversion_rate": 0.85})


class HistoricalRatesViewTest(APITestCase):
    def setUp(self):
        self.currency = Currency.objects.create(code="USD", name="Dollar", rate=Decimal("1.000000"))

    @patch("converter.services.requests.get")
    def test_fetch_historical_rates_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "success": True,
            "quotes": {"USDEUR": 0.85},
        }
        Currency.objects.create(code="EUR", name="Euro", rate=Decimal("0.850000"))

        response = self.client.post(
            reverse("historical-rates"),
            data={"date": "2025-01-01"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
