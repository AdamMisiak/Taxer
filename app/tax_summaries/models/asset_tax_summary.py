from django.db import models

from tax_summaries.models import BaseTaxSummary


class AsssetTaxSummary(BaseTaxSummary):
    revenue = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    profit_or_loss = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)


    class Meta:
        verbose_name = "Asset tax summary ➕"
        verbose_name_plural = "Asset tax summaries ➕"

    def __str__(self):
        return f"{AsssetTaxSummary.__name__} - {self.year} - Tax: {self.tax} PLN"
    
    def save(self, *args, **kwargs):

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(AsssetTaxSummary, self).save(*args, **kwargs)
