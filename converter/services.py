import requests
from datetime import datetime
from django.db import transaction
from decimal import Decimal
from .models import Currency, ConversionLog, HistoricalRate
from django.conf import settings

# API configuration
CURRENCY_API_URL = "http://api.currencylayer.com/live"
CURRENCY_API_KEY = settings.CURRENCY_API_KEY


@transaction.atomic
def fetch_currency_rates():
    """
    Fetch latest currency exchange rates from the external API and update the Currency table.
    """
    response = requests.get(CURRENCY_API_URL, params={"access_key": CURRENCY_API_KEY})
    data = response.json()

    if not data.get("success"):
        raise Exception("Failed to fetch currency rates: " + data.get("error", {}).get("info", "Unknown error"))

    # Parse and update rates
    quotes = data["quotes"]
    for code, rate in quotes.items():
        # The code from API has "USD" prefix, e.g., "USDEUR"
        currency_code = code[3:]
        Currency.objects.update_or_create(
            code=currency_code,
            defaults={"rate": rate, "last_updated": datetime.utcnow()},
        )


def convert_currency(from_currency_code, to_currency_code, amount):
    """
    Perform currency conversion between two currencies using the latest rates.
    Logs the conversion details in the ConversionLog table.

    :param from_currency_code: ISO code of the source currency (e.g., "USD").
    :param to_currency_code: ISO code of the target currency (e.g., "EUR").
    :param amount: Amount to be converted.
    :return: The converted amount and the conversion rate used.
    """
    try:
        # Get rates for the source and target currencies
        try:
            from_currency = Currency.objects.get(code=from_currency_code)
        except Currency.DoesNotExist:
            raise ValueError(f"Currency not found: {from_currency_code}")
        
        try:
            to_currency = Currency.objects.get(code=to_currency_code)
        except Currency.DoesNotExist:
            raise ValueError(f"Currency not found: {to_currency_code}")
        
        # Ensure the amount is a Decimal for consistent calculations
        amount = Decimal(amount)

        # Calculate conversion rate and result
        conversion_rate = to_currency.rate / from_currency.rate
        converted_amount = amount * conversion_rate

        # Log the conversion
        ConversionLog.objects.create(
            from_currency=from_currency,
            to_currency=to_currency,
            amount=amount,
            converted_amount=converted_amount,
            conversion_rate=conversion_rate,
        )

        return {"converted_amount": float(converted_amount), "conversion_rate": float(conversion_rate)}

    except Currency.DoesNotExist as e:
        raise ValueError(f"Currency not found: {e}")


@transaction.atomic
def fetch_historical_rates(date):
    """
    Fetch historical currency rates for a given date and update the HistoricalRate table.
    This uses the currencylayer API's historical endpoint.

    :param date: The date for which to fetch historical rates (in "YYYY-MM-DD" format).
    """
    url = f"http://api.currencylayer.com/historical"
    response = requests.get(url, params={"access_key": CURRENCY_API_KEY, "date": date})
    data = response.json()

    if not data.get("success"):
        raise Exception("Failed to fetch historical rates: " + data.get("error", {}).get("info", "Unknown error"))

    # Parse and save historical rates
    quotes = data["quotes"]
    for code, rate in quotes.items():
        # The code from API has "USD" prefix, e.g., "USDEUR"
        currency_code = code[3:]
        currency = Currency.objects.get(code=currency_code)
        HistoricalRate.objects.update_or_create(
            currency=currency,
            rate_date=datetime.strptime(date, "%Y-%m-%d").date(),
            defaults={"rate": rate},
        )
