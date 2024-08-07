from django.db import models
from django.conf import settings
from utils.models import Broker
from django.utils.html import format_html

# from .currency_rate import CurrencyRate
from .withholding_tax import WithholdingTax

from utils.choices import AssetType, TransactionSide, Currency, TransactionType
from transactions.models import BaseTransaction


class AssetTransaction(BaseTransaction):
    side = models.CharField(max_length=8, choices=TransactionSide.choices, blank=True)
    type = models.CharField(max_length=16, choices=TransactionType.choices, blank=True)
    
    price = models.FloatField()
    fee = models.FloatField()
    quantity = models.FloatField()

    value = models.FloatField()
    full_value = models.FloatField(db_comment="Value of assets including fee")

    value_pln = models.FloatField()
    full_value_pln = models.FloatField(db_comment="Value of assets including fee in PLN")

    class Meta:
        verbose_name = "Asset transaction 💸"
        verbose_name_plural = "Asset transactions 💸"
        unique_together = ("asset_name", "side", "price", "quantity", "executed_at", "raw_data")

    def __str__(self):
        return f"{AssetTransaction.__name__} - {self.side} {self.quantity} {self.asset_name} @ {self.price} {self.currency} ({self.executed_at.date()})"

    def save(self, *args, **kwargs):
        #NOTE a co jak bedize ETF?
        self.asset_type = AssetType.STOCKS.value

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(AssetTransaction, self).save(*args, **kwargs)
