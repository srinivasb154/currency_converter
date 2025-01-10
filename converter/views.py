from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Currency, ConversionLog, HistoricalRate
from .serializers import CurrencySerializer, ConversionLogSerializer, HistoricalRateSerializer
from .services import fetch_currency_rates, convert_currency, fetch_historical_rates

import logging

logger = logging.getLogger(__name__)


class CurrencyListView(APIView):
    """
    API endpoint to list all available currencies and their latest exchange rates.
    """
    def get(self, request):
        currencies = Currency.objects.all()
        serializer = CurrencySerializer(currencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ConvertCurrencyView(APIView):
    """
    API endpoint to perform currency conversion.
    """
    def post(self, request):
        data = request.data
        logger.debug(f"Request Data: {data}")  # Log the incoming request data
        from_currency = data.get("from_currency")
        to_currency = data.get("to_currency")
        amount = data.get("amount")

        if not all([from_currency, to_currency, amount]):
            return Response(
                {"error": "from_currency, to_currency, and amount are required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            amount = float(amount)
            result = convert_currency(from_currency, to_currency, amount)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"ValueError: {e}")  # Log the error
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")  # Log unexpected errors
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchCurrencyRatesView(APIView):
    """
    API endpoint to manually fetch and update the latest currency exchange rates.
    """
    def post(self, request):
        try:
            fetch_currency_rates()
            return Response({"message": "Currency rates updated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistoricalRatesView(APIView):
    """
    API endpoint to fetch and store historical currency exchange rates for a specific date.
    """
    def post(self, request):
        date = request.data.get("date")  # Expected format: YYYY-MM-DD

        if not date:
            return Response({"error": "The 'date' field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fetch_historical_rates(date)
            historical_rates = HistoricalRate.objects.filter(rate_date=date)
            serializer = HistoricalRateSerializer(historical_rates, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConversionLogView(APIView):
    """
    API endpoint to retrieve the list of logged currency conversions.
    """
    def get(self, request):
        logs = ConversionLog.objects.all().order_by("-timestamp")
        serializer = ConversionLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
