from django.db import models

from .currency_rate import CurrencyRate

CURRENCY_CHOCIES = [
    ("USD", "USD"),
    ("PLN", "PLN"),
    ("EUR", "EUR"),
    ("RUB", "RUB"),
]



class WithholdingTax(models.Model):
    # NOTE user
    # owner = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    # )
    # NOTE broker
    # broker = models.relation(max_length=100, default="API")
    asset_name = models.CharField(max_length=124)
    value = models.FloatField()
    value_pln = models.FloatField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOCIES)
    previous_day_currency_rate = models.ForeignKey(CurrencyRate, related_name="withholding_taxes", on_delete=models.RESTRICT, blank=True, null=True)

    paid_at = models.DateField()

    class Meta:
        verbose_name = "Withholding Tax"
        verbose_name_plural = "Withholding Taxes"

    def __str__(self):
        return (
            f"{self.asset_name} {self.value} {self.currency} - {self.paid_at}"
        )

    def save(self, *args, **kwargs):
        if self.id is not None:
            print(f"🆕 Updated WithholdingTax object: {self}")
        else:
            print(f"✅ Created WithholdingTax object: {self}")
        super(WithholdingTax, self).save(*args, **kwargs)
