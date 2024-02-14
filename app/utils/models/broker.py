from django.db import models


class Broker(models.Model):
    name = models.CharField(max_length=124)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Broker"
        verbose_name_plural = "Brokers"

    def __str__(self):
        return f"{self.name}"
