from django.db import models
from django.conf import settings
from utils.models import Broker
from django.utils.html import format_html

# from .currency_rate import CurrencyRate
from .withholding_tax import WithholdingTax

from utils.choices import AssetType, TransactionSide, OptionType
from transactions.models import BaseTransaction


class OptionTransaction(BaseTransaction):
    side = models.CharField(max_length=8, choices=TransactionSide.choices, blank=True)
    
    price = models.FloatField()
    fee = models.FloatField()
    quantity = models.FloatField()

    base_instrument = models.CharField(max_length=10)
    option_type = models.CharField(max_length=4, choices=OptionType.choices, blank=True)
    strike_price = models.FloatField(null=True, blank=True)
    expired = models.BooleanField(default=False)

    value = models.FloatField()
    full_value = models.FloatField(db_comment="Value of assets including fee")

    value_pln = models.FloatField()
    full_value_pln = models.FloatField(db_comment="Value of assets including fee in PLN")


    class Meta:
        verbose_name = "Option transaction 💸"
        verbose_name_plural = "Option transactions 💸"
        unique_together = ("asset_name", "side", "price", "quantity", "executed_at")

    def __str__(self):
        return f"{OptionTransaction.__name__} - {self.side} {self.option_type} {self.quantity} {self.asset_name} @ {self.price} {self.currency}{' (Expired)' if self.expired else ''} ({self.executed_at.date()})"

    def save(self, *args, **kwargs):
        self.asset_type = AssetType.OPTIONS.value

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(OptionTransaction, self).save(*args, **kwargs)
