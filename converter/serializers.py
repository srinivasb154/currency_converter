from rest_framework import serializers
from .models import Currency, HistoricalRate, ConversionLog

class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for the Currency model."""
    
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'rate', 'last_updated']


class HistoricalRateSerializer(serializers.ModelSerializer):
    """Serializer for the HistoricalRate model."""
    
    currency = serializers.StringRelatedField()  # Display the currency name/code

    class Meta:
        model = HistoricalRate
        fields = ['id', 'currency', 'rate', 'rate_date']


class ConversionLogSerializer(serializers.ModelSerializer):
    """Serializer for the ConversionLog model."""
    
    from_currency = serializers.StringRelatedField()  # Display source currency name/code
    to_currency = serializers.StringRelatedField()    # Display target currency name/code

    class Meta:
        model = ConversionLog
        fields = [
            'id', 
            'from_currency', 
            'to_currency', 
            'amount', 
            'converted_amount', 
            'conversion_rate', 
            'timestamp'
        ]
