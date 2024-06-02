from django.db import models

from transactions.models import DividendTransaction, WithholdingTaxTransaction
from tax_calculations.models import BaseTaxCalculation


class DividendTaxCalculation(BaseTaxCalculation):
    # NOTE one to one relation?
    withholding_tax_transaction = models.ForeignKey(
        WithholdingTaxTransaction,
        related_name="tax_calculation",
        on_delete=models.CASCADE,
    )
    # NOTE one to one relation?
    dividend_transaction = models.ForeignKey(
        DividendTransaction,
        related_name="tax_calculation",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Dividend tax calculation 🧮"
        verbose_name_plural = "Dividend tax calculations 🧮"

    def __str__(self):
        return f"{DividendTaxCalculation.__name__} - {self.opening_transaction} <> {self.closing_transaction} Tax: {self.tax} PLN"
    
    def save(self, *args, **kwargs):

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(DividendTaxCalculation, self).save(*args, **kwargs)
