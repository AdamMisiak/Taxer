from django.db import models

class CurrencyRateFile(models.Model):
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Currency rate file 💵"
        verbose_name_plural = "Currency rate files 💵"

    def __str__(self):
        return f"{CurrencyRateFile.__name__} - {self.file}"

    def save(self, *args, **kwargs):
        from files.tasks import save_data_from_currency_rate_file
        
        if self.id is not None:
            print(f"♻️  Updated: {self}\n")
        else:
            print(f"✅ Created: {self}\n")

        super(CurrencyRateFile, self).save(*args, **kwargs)

        save_data_from_currency_rate_file.delay(self.id)