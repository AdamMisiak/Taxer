from django.db import models

from tax_summaries.models import BaseTaxSummary


class DividendTaxSummary(BaseTaxSummary):
    general_tax_summary = models.OneToOneField(
        "GeneralTaxSummary",
        related_name="dividend_tax_summaries",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    revenue = models.FloatField(blank=True, null=True)
    tax_paid = models.FloatField(blank=True, null=True)
    profit_or_loss = models.FloatField(blank=True, null=True)
    # NOTE remaining tax to paid in Poland
    tax = models.FloatField(blank=True, null=True)


    class Meta:
        verbose_name = "Dividend tax summary ➕"
        verbose_name_plural = "Dividend tax summaries ➕"

    def __str__(self):
        return f"{DividendTaxSummary.__name__} - {self.year} - Tax: {self.tax} PLN"
    
    def save(self, *args, **kwargs):

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(DividendTaxSummary, self).save(*args, **kwargs)
