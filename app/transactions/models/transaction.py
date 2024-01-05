from django.db import models

SIDE_CHOICES = [
    ("Buy", "Buy"),
    ("Sell", "Sell"),
]

ASSET_TYPE_CHOICES = [
    ("Stocks", "Stocks"),
    ("Bonds", "Bonds"),
    ("Equity and Index Options", "Options"),
    ("ETFs", "ETFs"),
]

CURRENCY_CHOCIES = [
    ("USD", "USD"),
    ("PLN", "PLN"),
    ("EUR", "EUR"),
    ("RUB", "RUB"),
]

OPTION_TYPE_CHOICES = [
    ("CALL", "CALL"),
    ("PUT", "PUT"),
]

class Transaction(models.Model):
    # NOTE user
    # owner = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    # )
    # NOTE broker
    # broker = models.relation(max_length=100, default="API")
    asset = models.CharField(max_length=124)
    side = models.CharField(
        max_length=8, choices=SIDE_CHOICES
    )
    asset_type = models.CharField(
        max_length=124, choices=ASSET_TYPE_CHOICES
    )

    price = models.FloatField()
    quantity = models.FloatField()
    value =  models.FloatField()
    value_pln =  models.FloatField()
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOCIES
    )
    fee = models.FloatField()

    option_type = models.CharField(
        blank=True, max_length=4, choices=OPTION_TYPE_CHOICES
    )
    strike_price = models.FloatField(null=True, blank=True)

    executed_at = models.DateTimeField()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        unique_together = ('asset', 'side', "price", "quantity", "executed_at")


    def __str__(self):
        return f"{self.side} {self.quantity} {self.asset} @ {self.price} {self.currency} - {self.executed_at.date()}"
