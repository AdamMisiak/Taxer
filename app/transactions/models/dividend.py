from django.db import models

from .currency_rate import CurrencyRate

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
    value = models.FloatField()
    value_pln = models.FloatField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOCIES)
    previous_day_currency_rate = models.ForeignKey(CurrencyRate, related_name="dividends", on_delete=models.RESTRICT, blank=True, null=True)
    withholding_tax = models.ForeignKey(CurrencyRate, on_delete=models.CASCADE, blank=True, null=True)

    # NOTE change to the time zone aware
    received_at = models.DateField()

    class Meta:
        verbose_name = "Dividend"
        verbose_name_plural = "Dividends"

    def __str__(self):
        return (
            f"{self.asset_name} {self.value} {self.currency} - {self.received_at}"
        )

    def save(self, *args, **kwargs):
        # NOTE add different message when updating with different
        if self.id is not None:
            print(f"🆕 Updated Dividend object: {self}")
        else:
            print(f"✅ Created Dividend object: {self}")
        super(Dividend, self).save(*args, **kwargs)
