from django.db import models
from django.conf import settings
from utils.models import Broker
from django.utils.html import format_html

from .withholding_tax import WithholdingTax
from rates.models import CurrencyRate

from utils.choices import AssetType, TransactionSide, Currency
# SIDE_CHOICES = [
#     ("Buy", "Buy"),
#     ("Sell", "Sell"),
# ]

# ASSET_TYPE_CHOICES = [
#     ("Stocks", "Stocks"),
#     ("Bonds", "Bonds"),
#     ("Equity and Index Options", "Options"),
#     ("ETFs", "ETFs"),
#     ("Forex", "Forex"),
#     ("Dividends", "Dividends"),
#     ("Withholding Tax", "Withholding Tax"),
#     ("Others", "Others"),
# ]

# CURRENCY_CHOCIES = [
#     ("USD", "USD"),
#     ("PLN", "PLN"),
#     ("EUR", "EUR"),
#     ("RUB", "RUB"),
# ]

OPTION_TYPE_CHOICES = [
    ("CALL", "CALL"),
    ("PUT", "PUT"),
]


class BaseTransaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    broker = models.ForeignKey(Broker, blank=True, null=True, on_delete=models.CASCADE)
    previous_day_currency_rate = models.ForeignKey(CurrencyRate, related_name="transactions2", on_delete=models.RESTRICT, blank=True, null=True)

    asset_name = models.CharField(max_length=124)

    asset_type = models.CharField(max_length=124, choices=AssetType.choices)
    # NOTE div won't have side
    side = models.CharField(max_length=8, choices=TransactionSide.choices, blank=True)
    currency = models.CharField(max_length=3, choices=Currency.choices)

    executed_at = models.DateTimeField(blank=True, null=True)

    # price = models.FloatField(null=True, blank=True)
    # quantity = models.FloatField(null=True, blank=True)
    # value = models.FloatField()
    # full_value = models.FloatField(null=True, blank=True)
    # value_pln = models.FloatField()
    # full_value_pln = models.FloatField(null=True, blank=True)
    # fee = models.FloatField(null=True, blank=True)

    # # Option only
    # option_type = models.CharField(blank=True, max_length=4, choices=OPTION_TYPE_CHOICES)
    # strike_price = models.FloatField(null=True, blank=True)

    # # Dividend only
    # value_per_share = models.FloatField(blank=True, null=True)
    # withholding_tax = models.ForeignKey("Transaction", related_name="dividends", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True
        # verbose_name = "Base transaction"
        # verbose_name_plural = "Base transactions"


    def colored_side(self):
        color_code = "008000" if self.side == TransactionSide.BUY.value else "D2042D"
        return format_html(f'<span style="color: #{color_code};">{self.side}</span>')

    # def __str__(self):
    #     if self.asset_type in ["Dividends", "Withholding Tax", "Others"]:
    #         return (
    #             f"{self.asset_name} {self.value} {self.currency} - {self.executed_at}"
    #         )
    #     elif self.asset_type == "Equity and Index Options":
    #         return (
    #             f"{self.side} {self.option_type} {self.quantity} {self.asset_name} @ {self.price} {self.currency}"
    #         )
    #     return (
    #         f"{self.side} {self.quantity} {self.asset_name} @ {self.price} {self.currency} - {self.executed_at.date()}"
    #     )

    # def save(self, *args, **kwargs):
    #     raise Exception("ADD HERE EXCEPTION")
    #     # NOTE add different message when updating with different
    #     if self.id is not None:
    #         print(f"🆕 Updated Transaction object ({self.asset_type}): {self}\n")
    #     else:
    #         print(f"✅ Created Transaction object ({self.asset_type}): {self}\n")
    #     super(Transaction, self).save(*args, **kwargs)
