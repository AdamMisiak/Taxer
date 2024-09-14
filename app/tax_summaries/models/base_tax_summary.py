from django.db import models


class BaseTaxSummary(models.Model):
    year = models.IntegerField(unique=True)

    class Meta:
        abstract = True

    # year = models.IntegerField(unique=True)
    # revenue_equity = models.FloatField(blank=True, null=True)
    # revenue_dividend = models.FloatField(blank=True, null=True)
    # cost_equity = models.FloatField(blank=True, null=True)
    # tax_paid_dividend = models.FloatField(blank=True, null=True)
    # tax_equity = models.FloatField(blank=True, null=True)
    # tax_dividend = models.FloatField(blank=True, null=True)