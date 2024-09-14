from django.db import models

from tax_summaries.models import BaseTaxSummary


class AssetTaxSummary(BaseTaxSummary):
    general_tax_summary = models.OneToOneField(
        "GeneralTaxSummary",
        related_name="asset_tax_summaries",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    revenue = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    profit_or_loss = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)


    class Meta:
        verbose_name = "Asset tax summary ➕"
        verbose_name_plural = "Asset tax summaries ➕"

    def __str__(self):
        return f"{AssetTaxSummary.__name__} - {self.year} - Tax: {self.tax} PLN"
    
    def save(self, *args, **kwargs):

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(AssetTaxSummary, self).save(*args, **kwargs)
