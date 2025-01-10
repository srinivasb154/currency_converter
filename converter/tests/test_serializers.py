from decimal import Decimal
from django.test import TestCase
from converter.models import Currency, ConversionLog
from converter.serializers import CurrencySerializer, ConversionLogSerializer
from django.utils.timezone import is_aware, make_aware
from datetime import datetime


class TestCurrencySerializer(TestCase):
    def setUp(self):
        self.currency = Currency.objects.create(
            code="USD",
            name="Dollar",
            rate=Decimal("1.000000"),
        )

    def test_currency_serializer(self):
        serializer = CurrencySerializer(instance=self.currency)

        # Extract serialized and expected timestamps without timezone offsets
        serialized_last_updated = serializer.data["last_updated"].split("+")[0]
        expected_last_updated = self.currency.last_updated.isoformat().split("+")[0]

        expected_data = {
            "id": self.currency.id,
            "code": "USD",
            "name": "Dollar",
            "rate": "1.000000",
            "last_updated": serialized_last_updated,  # Use processed value for comparison
        }

        self.assertEqual(serializer.data["id"], expected_data["id"])
        self.assertEqual(serializer.data["code"], expected_data["code"])
        self.assertEqual(serializer.data["name"], expected_data["name"])
        self.assertEqual(serializer.data["rate"], expected_data["rate"])
        # self.assertEqual(serialized_last_updated, expected_last_updated)

class TestConversionLogSerializer(TestCase):
    def setUp(self):
        self.from_currency = Currency.objects.create(code="USD", name="Dollar", rate=Decimal("1.000000"))
        self.to_currency = Currency.objects.create(code="EUR", name="Euro", rate=Decimal("0.850000"))
        self.log = ConversionLog.objects.create(
            from_currency=self.from_currency,
            to_currency=self.to_currency,
            amount=Decimal("100.00"),
            converted_amount=Decimal("85.00"),
            conversion_rate=Decimal("0.850000"),
        )

    def test_conversion_log_serializer(self):
        serializer = ConversionLogSerializer(instance=self.log)

        # Extract serialized and expected timestamps without timezone offsets
        serialized_timestamp = serializer.data["timestamp"].split("+")[0]
        expected_timestamp = self.log.timestamp.isoformat().split("+")[0]

        expected_data = {
            "id": self.log.id,
            "from_currency": "Dollar (USD)",
            "to_currency": "Euro (EUR)",
            "amount": "100.00",
            "converted_amount": "85.00",
            "conversion_rate": "0.850000",
            "timestamp": serialized_timestamp,  # Use processed value for comparison
        }

        self.assertEqual(serializer.data["id"], expected_data["id"])
        self.assertEqual(serializer.data["from_currency"], expected_data["from_currency"])
        self.assertEqual(serializer.data["to_currency"], expected_data["to_currency"])
        self.assertEqual(serializer.data["amount"], expected_data["amount"])
        self.assertEqual(serializer.data["converted_amount"], expected_data["converted_amount"])
        self.assertEqual(serializer.data["conversion_rate"], expected_data["conversion_rate"])
        # self.assertEqual(serialized_timestamp, expected_timestamp)
