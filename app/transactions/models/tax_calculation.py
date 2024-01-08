
from django.db import models
from .transaction import Transaction

class TaxCalculation(models.Model):
    opening_transaction = models.ForeignKey(
        Transaction, related_name="as_opening_calculation",
        on_delete=models.CASCADE, blank=True, null=True
    )
    closing_transaction = models.ForeignKey(
        Transaction, related_name="as_closing_calculation",
        on_delete=models.CASCADE, blank=True, null=True
    )
    revenue = models.FloatField()
    cost = models.FloatField()
    profit_or_loss = models.FloatField()
    tax = models.FloatField()

    class Meta:
        verbose_name = "Tax calculation"
        verbose_name_plural = "Tax calculations"


    def __str__(self):
        return f"{self.opening_transaction} - {self.closing_transaction}"
