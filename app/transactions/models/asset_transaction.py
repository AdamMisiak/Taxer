from django.db import models
from django.conf import settings
from utils.models import Broker
from django.utils.html import format_html

from .currency_rate import CurrencyRate
from .withholding_tax import WithholdingTax

from utils.choices import AssetType, TransactionSide, Currency
from transactions.models import BaseTransaction


class AssetTransaction(BaseTransaction):
    # NOTE why null and blank?
    price = models.FloatField(null=True, blank=True)
    fee = models.FloatField(null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)

    value = models.FloatField()
    full_value = models.FloatField(db_comment="Value of assets including fee", null=True, blank=True)

    value_pln = models.FloatField()
    full_value_pln = models.FloatField(db_comment="Value of assets including fee in PLN", null=True, blank=True)

    class Meta:
        verbose_name = "Asset transaction"
        verbose_name_plural = "Asset transactions"
        unique_together = ("asset_name", "side", "price", "quantity", "executed_at")

    # def __str__(self):
    #     print([f.name for f in AssetTransaction._meta.get_fields()])
    #     return f"{AssetTransaction.__name__} - {self.side} {self.quantity} {self.asset_name} @ {self.price} {self.currency} - {self.executed_at.date()}"

    def save(self, *args, **kwargs):
        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(AssetTransaction, self).save(*args, **kwargs)
