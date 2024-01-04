
from django.db import models


class Tax(models.Model):
    year = models.IntegerField(unique=True)
    to_pay = models.FloatField()

    class Meta:
        verbose_name = "Tax"
        verbose_name_plural = "Taxes"


    def __str__(self):
        return f"{self.year} - {self.to_pay}"
