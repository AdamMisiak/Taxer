from django.db import models
from .withholding_tax import WithholdingTax

from utils.choices import AssetType
from transactions.models import BaseTransaction

class WithholdingTaxTransaction(BaseTransaction):
    value = models.FloatField()
    value_pln = models.FloatField()

    raw_data = models.TextField(max_length=1256, blank=True, null=True)

    class Meta:
        verbose_name = "Withholding Tax transaction"
        verbose_name_plural = "Withholding Tax transactions"
        # unique_together = ("asset_name", "value", "currency", "executed_at")

    def __str__(self):
        return f"{WithholdingTax.__name__} - {self.asset_name} {self.value} {self.currency} ({self.executed_at.date()})"

    def save(self, *args, **kwargs):
        self.asset_type = AssetType.WITHHOLDING_TAX.value

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(WithholdingTax, self).save(*args, **kwargs)