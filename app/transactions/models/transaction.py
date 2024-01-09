from django.db import models
from .currency_rate import CurrencyRate
from django.utils.html import format_html

SIDE_CHOICES = [
    ("Buy", "Buy"),
    ("Sell", "Sell"),
]

ASSET_TYPE_CHOICES = [
    ("Stocks", "Stocks"),
    ("Bonds", "Bonds"),
    ("Equity and Index Options", "Options"),
    ("ETFs", "ETFs"),
    ("Forex", "Forex"),
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
    asset_name = models.CharField(max_length=124)
    asset_type = models.CharField(
        max_length=124, choices=ASSET_TYPE_CHOICES
    )
    side = models.CharField(
        max_length=8, choices=SIDE_CHOICES
    )

    price = models.FloatField()
    quantity = models.FloatField()
    value =  models.FloatField()
    value_pln =  models.FloatField()
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOCIES
    )
    previous_day_currency_rate = models.ForeignKey(
        CurrencyRate,
        on_delete=models.RESTRICT, blank=True, null=True
    )
    fee = models.FloatField()

    option_type = models.CharField(
        blank=True, max_length=4, choices=OPTION_TYPE_CHOICES
    )
    strike_price = models.FloatField(null=True, blank=True)

    # NOTE change to the time zone aware 
    executed_at = models.DateTimeField()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        unique_together = ('asset_name', 'side', "price", "quantity", "executed_at")

    def colored_side(self):
        color_code = "008000" if self.side == "Buy" else "D2042D"
        return format_html(
            f'<span style="color: #{color_code};">{self.side}</span>'
        )

    def __str__(self):
        return f"{self.side} {self.quantity} {self.asset_name} @ {self.price} {self.currency} - {self.executed_at.date()}"

    def save(self, *args, **kwargs):
        # NOTE add different message when updating with different 
        if self.id is not None:
            print(f"🆕 Updated Transaction object: {self}")
        else:
            print(f"✅ Created Transaction object: {self}")
        super(Transaction, self).save(*args, **kwargs)