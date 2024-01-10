from django.contrib import admin
from transactions.models import CurrencyRate, ImportFile, TaxCalculation, TaxSummary, Transaction


class ImportFileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_at")

class TaxCalculationOpeningInline(admin.StackedInline):
    verbose_name_plural = "Tax Opening Calculations"
    model = TaxCalculation
    fk_name = "closing_transaction"
    extra = 0


class TaxCalculationClosingInline(admin.StackedInline):
    verbose_name_plural = "Tax Closing Calculations"
    model = TaxCalculation
    fk_name = "opening_transaction"
    extra = 0


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "asset_name",
        "colored_side",
        "asset_type",
        "price",
        "quantity",
        "value",
        "value_pln",
        "currency",
        "fee",
        "executed_at",
    )
    list_filter = ("side", "asset_type", "currency")
    search_fields = ("asset_name", "asset_type")
    ordering = ("-executed_at", "asset_name", "fee", "quantity", "value", "value_pln")
    inlines = [
        TaxCalculationOpeningInline,
        TaxCalculationClosingInline,
    ]


class TaxSummaryAdmin(admin.ModelAdmin):
    list_display = ("year", "tax", "revenue", "cost")
    ordering = ("-year", "tax", "revenue", "cost")


class TaxCalculationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "opening_transaction",
        "closing_transaction",
        "tax",
        "revenue",
        "cost",
        "profit_or_loss",
    )
    ordering = ("tax", "revenue", "profit_or_loss", "cost")


class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ("date", "usd", "eur", "gbp")
    ordering = ("-date", "usd", "eur", "gbp")


admin.site.register(ImportFile, ImportFileAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CurrencyRate, CurrencyRateAdmin)
admin.site.register(TaxSummary, TaxSummaryAdmin)
admin.site.register(TaxCalculation, TaxCalculationAdmin)
