from django.db import models
from django.conf import settings
from utils.models import Broker
from django.utils.html import format_html

from .currency_rate import CurrencyRate
from .withholding_tax import WithholdingTax

from utils.choices import AssetType, TransactionSide, Currency
from transactions.models import BaseTransaction


class AssetTransaction(BaseTransaction):
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

    def __str__(self):
        return (
            f"{self.side} {self.quantity} {self.asset_name} @ {self.price} {self.currency} - {self.executed_at.date()}"
        )