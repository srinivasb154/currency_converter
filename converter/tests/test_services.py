from django.test import TestCase
from unittest.mock import patch
from converter.models import Currency, ConversionLog, HistoricalRate
from converter.services import fetch_currency_rates, convert_currency, fetch_historical_rates
from decimal import Decimal
from datetime import datetime


class TestFetchCurrencyRates(TestCase):
    @patch("converter.services.requests.get")
    def test_fetch_currency_rates_success(self, mock_get):
        mock_get.return_value.json.return_value = {
            "success": True,
            "quotes": {"USDUSD": 1.0, "USDEUR": 0.85, "USDGBP": 0.75},
        }

        fetch_currency_rates()

        self.assertTrue(Currency.objects.filter(code="EUR").exists())
        self.assertTrue(Currency.objects.filter(code="GBP").exists())
        self.assertEqual(Currency.objects.get(code="EUR").rate, Decimal("0.85"))

    @patch("converter.services.requests.get")
    def test_fetch_currency_rates_failure(self, mock_get):
        mock_get.return_value.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}

        with self.assertRaises(Exception) as context:
            fetch_currency_rates()

        self.assertIn("Failed to fetch currency rates", str(context.exception))


class TestConvertCurrency(TestCase):
    def setUp(self):
        self.usd = Currency.objects.create(code="USD", name="United States Dollar", rate=1.0)
        self.eur = Currency.objects.create(code="EUR", name="Euro", rate=0.85)

    def test_convert_currency_success(self):
        result = convert_currency("USD", "EUR", 100)
        self.assertEqual(result["converted_amount"], 85.0)
        self.assertEqual(result["conversion_rate"], 0.85)
        self.assertTrue(ConversionLog.objects.filter(from_currency=self.usd, to_currency=self.eur).exists())

    def test_convert_currency_invalid_currency(self):
        with self.assertRaises(ValueError):
            convert_currency("USD", "ABC", 100)


class TestFetchHistoricalRates(TestCase):
    @patch("converter.services.requests.get")
    def test_fetch_historical_rates_success(self, mock_get):
        self.usd = Currency.objects.create(code="USD", name="United States Dollar", rate=1.0)
        self.eur = Currency.objects.create(code="EUR", name="Euro", rate=0.85)

        mock_get.return_value.json.return_value = {
            "success": True,
            "quotes": {"USDUSD": 1.0, "USDEUR": 0.83},
        }

        fetch_historical_rates("2025-01-01")
        self.assertTrue(HistoricalRate.objects.filter(currency=self.eur, rate_date="2025-01-01").exists())

    @patch("converter.services.requests.get")
    def test_fetch_historical_rates_failure(self, mock_get):
        mock_get.return_value.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}

        with self.assertRaises(Exception) as context:
            fetch_historical_rates("2025-01-01")

        self.assertIn("Failed to fetch historical rates", str(context.exception))
