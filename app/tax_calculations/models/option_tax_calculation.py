from django.db import models

from transactions.models import OptionTransaction
from tax_calculations.models import BaseTaxCalculation


class OptionTaxCalculation(BaseTaxCalculation):
    opening_transaction = models.ForeignKey(
        OptionTransaction,
        related_name="as_opening_calculation",
        on_delete=models.CASCADE,
    )
    closing_transaction = models.ForeignKey(
        OptionTransaction,
        related_name="as_closing_calculation",
        on_delete=models.CASCADE,
    )
    
    quantity = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Option tax calculation 🧮"
        verbose_name_plural = "Option tax calculations 🧮"

    def __str__(self):
        return f"{OptionTaxCalculation.__name__} - {self.opening_transaction} <> {self.closing_transaction} Tax: {self.tax} PLN"
    
    def save(self, *args, **kwargs):

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(OptionTaxCalculation, self).save(*args, **kwargs)
