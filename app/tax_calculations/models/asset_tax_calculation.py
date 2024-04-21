from django.db import models

from transactions.models import AssetTransaction


class AssetTaxCalculation(models.Model):
    opening_transaction = models.ForeignKey(
        AssetTransaction,
        related_name="as_opening_calculation",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    quantity = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Asset tax calculation 🧮"
        verbose_name_plural = "Asset tax calculations 🧮"

    def __str__(self):
        custom_quantity = f"Custom quantity: {self.quantity}" if self.quantity is not None else ""
        return f"{AssetTaxCalculation.__name__} - {self.opening_transaction} <> {self.closing_transaction} {custom_quantity} Tax: {self.tax} PLN"
    
    def save(self, *args, **kwargs):

        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(AssetTransaction, self).save(*args, **kwargs)
