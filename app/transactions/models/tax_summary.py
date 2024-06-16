from django.db import models


class TaxSummary(models.Model):
    year = models.IntegerField(unique=True)
    revenue_equity = models.FloatField(blank=True, null=True)
    revenue_dividend = models.FloatField(blank=True, null=True)
    cost_equity = models.FloatField(blank=True, null=True)
    tax_paid_dividend = models.FloatField(blank=True, null=True)
    tax_equity = models.FloatField(blank=True, null=True)
    tax_dividend = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "Tax summary"
        verbose_name_plural = "Tax summary"

    def __str__(self):
        return f"{self.year} - tax equity: {self.tax_equity} - tax dividend: {self.tax_dividend}"

    def save(self, *args, **kwargs):
        if self.id is not None:
            print(f"🆕 Updated TaxSummary object: {self}\n")
        else:
            print(f"✅ Created TaxSummary object: {self}\n")
        super(TaxSummary, self).save(*args, **kwargs)
