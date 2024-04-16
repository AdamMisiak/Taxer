from django.db import models

from utils.choices import AssetType
from transactions.models import BaseTransaction

class DividendTransaction(BaseTransaction):
    withholding_tax_transaction = models.OneToOneField("WithholdingTaxTransaction", related_name="dividend_transaction", on_delete=models.CASCADE, blank=True, null=True)

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