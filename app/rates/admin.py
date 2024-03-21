from django.contrib import admin
from rates.models import CurrencyRate


class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ("date", "usd", "eur", "gbp", "chf")
    ordering = ("-date", "usd", "eur", "gbp", "chf")

admin.site.register(CurrencyRate, CurrencyRateAdmin)
