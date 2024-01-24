from django.db import models

from .currency_rate import CurrencyRate
from .withholding_tax import WithholdingTax

CURRENCY_CHOCIES = [
    ("USD", "USD"),
    ("PLN", "PLN"),
    ("EUR", "EUR"),
    ("RUB", "RUB"),
]



class Dividend(models.Model):
    # NOTE user
    # owner = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    # )
    # NOTE broker
    # broker = models.relation(max_length=100, default="API")
    asset_name = models.CharField(max_length=124)
    value_per_share = models.FloatField(blank=True, null=True)
    value = models.FloatField()
    value_pln = models.FloatField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOCIES)
    previous_day_currency_rate = models.ForeignKey(CurrencyRate, related_name="dividends", on_delete=models.RESTRICT, blank=True, null=True)
    withholding_tax = models.ForeignKey(WithholdingTax, related_name="dividends", on_delete=models.CASCADE, blank=True, null=True)

    received_at = models.DateField()

    class Meta:
        verbose_name = "Dividend"
        verbose_name_plural = "Dividends"

    def __str__(self):
        return (
            f"{self.asset_name} {self.value} {self.currency} - {self.received_at}"
        )

    def save(self, *args, **kwargs):
        if self.id is not None:
            print(f"🆕 Updated Dividend object: {self}\n")
        else:
            print(f"✅ Created Dividend object: {self}\n")
        super(Dividend, self).save(*args, **kwargs)
