from transactions.models import ImportFile, Transaction, TaxSummary, CurrencyRate, TaxCalculation
from django.contrib import admin


class ImportFileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_at")
    # list_filter = ("author", "source")
    # search_fields = ("search_text", "author")
    # ordering = ("-created_at", "search_text", "author")


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("asset_name", "colored_side", "asset_type", "price", "quantity", "value", "value_pln", "currency", "fee", "executed_at")
    list_filter = ("side", "asset_type", "currency")
    search_fields = ("asset_name", "asset_type")
    ordering = ("-executed_at", "asset_name", "fee", "quantity", "value", "value_pln")

class TaxSummaryAdmin(admin.ModelAdmin):
    list_display = ("year", "tax", "revenue", "cost")
    ordering = ("-year", "tax", "revenue", "cost")

class TaxCalculationAdmin(admin.ModelAdmin):
    list_display = ("id", "opening_transaction", "closing_transaction", "tax", "revenue", "profit_or_loss", "cost")
    ordering = ("tax", "revenue", "profit_or_loss", "cost")

class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ("date", "usd", "eur", "gbp")
    ordering = ("-date", "usd", "eur", "gbp")

admin.site.register(ImportFile, ImportFileAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
admin.site.register(TaxSummary, TaxSummaryAdmin)
admin.site.register(TaxCalculation, TaxCalculationAdmin)