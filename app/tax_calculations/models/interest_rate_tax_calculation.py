from django.db import models

from transactions.models import InterestRateTransaction
from tax_calculations.models import BaseTaxCalculation
from tax_summaries.models import InterestRateTaxSummary


class InterestRateTaxCalculation(BaseTaxCalculation):
    tax_summary = models.ForeignKey(
        InterestRateTaxSummary,
        related_name="tax_calculations",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # NOTE one to one relation?
    interest_rate_transaction = models.ForeignKey(
        InterestRateTransaction,
        related_name="tax_calculation",
        on_delete=models.CASCADE,
    )

    quantity = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Interest rate tax calculation 🧮"
        verbose_name_plural = "Interest rate tax calculations 🧮"

    def __str__(self):
        return f"{InterestRateTaxCalculation.__name__} - {self.interest_rate_transaction} Tax: {self.tax} PLN"
    
    def save(self, *args, **kwargs):

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(InterestRateTaxCalculation, self).save(*args, **kwargs)
