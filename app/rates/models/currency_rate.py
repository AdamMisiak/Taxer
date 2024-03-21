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
        return f"{CurrencyRate.__name__} - {self.date} - {self.usd} USD"
    
    def save(self, *args, **kwargs):
        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(CurrencyRate, self).save(*args, **kwargs)