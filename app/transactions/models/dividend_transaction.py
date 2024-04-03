from django.db import models
from django.conf import settings
from utils.models import Broker
from django.utils.html import format_html

# from .currency_rate import CurrencyRate
from .withholding_tax import WithholdingTax

from utils.choices import AssetType, TransactionSide, Currency
from transactions.models import BaseTransaction

class DividendTransaction(BaseTransaction):
    # withholding_tax = models.ForeignKey("Transaction", related_name="dividends", on_delete=models.CASCADE, blank=True, null=True)

    value = models.FloatField()
    value_per_share = models.FloatField(blank=True, null=True)
    value_pln = models.FloatField()

    class Meta:
        verbose_name = "Dividend transaction"
        verbose_name_plural = "Dividend transactions"
        # unique_together = ("asset_name", "value", "currency", "executed_at")

    def __str__(self):
        return f"{DividendTransaction.__name__} - {self.asset_name} {self.value} {self.currency} ({self.executed_at.date()})"

    def save(self, *args, **kwargs):
        self.asset_type = AssetType.DIVIDENDS.value

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(DividendTransaction, self).save(*args, **kwargs)