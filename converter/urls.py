from django.urls import path
from .views import (
    CurrencyListView,
    ConvertCurrencyView,
    FetchCurrencyRatesView,
    HistoricalRatesView,
    ConversionLogView,
)

urlpatterns = [
    path("currencies/", CurrencyListView.as_view(), name="currency-list"),
    path("convert/", ConvertCurrencyView.as_view(), name="convert-currency"),
    path("fetch-rates/", FetchCurrencyRatesView.as_view(), name="fetch-currency-rates"),
    path("historical-rates/", HistoricalRatesView.as_view(), name="historical-rates"),
    path("conversion-logs/", ConversionLogView.as_view(), name="conversion-logs"),
]
