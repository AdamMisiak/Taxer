from django.db import models

from utils.choices import AssetType, TransactionSide
from transactions.models import BaseTransaction


class InterestRateTransaction(BaseTransaction):
    side = models.CharField(max_length=8, choices=TransactionSide.choices, blank=True)
    
    value = models.FloatField()
    value_pln = models.FloatField()

    class Meta:
        verbose_name = "Interest Rates transaction"
        verbose_name_plural = "Interest Rates transactions"

    def __str__(self):
        return f"{InterestRateTransaction.__name__} - {self.asset_name} {self.value} {self.currency} ({self.executed_at.date()})"

    def save(self, *args, **kwargs):
        self.asset_type = AssetType.OTHERS.value

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(InterestRateTransaction, self).save(*args, **kwargs)
