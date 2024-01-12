from django.db import models


class CurrencyRate(models.Model):
    date = models.DateField(unique=True)
    usd = models.FloatField()
    eur = models.FloatField()
    gbp = models.FloatField()
    chf = models.FloatField()
    rub = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Currency rate"
        verbose_name_plural = "Currency rates"

    def __str__(self):
        return f"{self.date} - {self.usd} USD"

    def save(self, *args, **kwargs):
        print(f"✅ Created CurrencyRate object: {self}")
        super(CurrencyRate, self).save(*args, **kwargs)
