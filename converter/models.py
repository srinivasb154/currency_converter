from django.db import models

class Currency(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    rate = models.DecimalField(max_digits=20, decimal_places=6)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class HistoricalRate(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=20, decimal_places=6)
    rate_date = models.DateField()

    def __str__(self):
        return f"{self.currency.code} - {self.rate_date}"

class ConversionLog(models.Model):
    from_currency = models.ForeignKey(Currency, related_name='from_currency', on_delete=models.CASCADE)
    to_currency = models.ForeignKey(Currency, related_name='to_currency', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    converted_amount = models.DecimalField(max_digits=20, decimal_places=2)
    conversion_rate = models.DecimalField(max_digits=20, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_currency.code} -> {self.to_currency.code}: {self.amount}"

