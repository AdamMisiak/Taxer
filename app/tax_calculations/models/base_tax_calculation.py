from django.db import models

# from .tax_summary import TaxSummary
from transactions.models import BaseTransaction
from django.utils.html import format_html


class BaseTaxCalculation(models.Model):
    # tax_summary = models.ForeignKey(
    #     TaxSummary,
    #     related_name="tax_calculations",
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )
    # opening_transaction = models.ForeignKey(
    #     Transaction,
    #     related_name="as_opening_calculation",
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )
    # closing_transaction = models.ForeignKey(
    #     BaseTransaction,
    #     related_name="as_closing_calculation",
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )
    revenue = models.FloatField()
    cost = models.FloatField()
    profit_or_loss = models.FloatField()

    tax_rate = models.FloatField(default=0.19)
    tax = models.FloatField()
    # quantity = models.FloatField(blank=True, null=True)

    class Meta:
        abstract = True

    def colored_tax(self):
        color_code = "008000" if self.tax > 0 else "D2042D"
        return format_html(f'<span style="color: #{color_code};">{self.tax}</span>')
    
    # def __str__(self):
    #     custom_quantity = f"Custom quantity: {self.quantity}" if self.quantity is not None else ""
    #     return f"{self.opening_transaction} <> {self.closing_transaction} {custom_quantity} Tax: {self.tax} PLN"

    # def save(self, *args, **kwargs):
    #     if self.id is not None:
    #         print(f"🆕 Updated TaxCalculation object: {self}")
    #     else:
    #         print(f"✅ Created TaxCalculation object: {self}")
    #     super(TaxCalculation, self).save(*args, **kwargs)
