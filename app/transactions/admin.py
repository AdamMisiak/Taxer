from django.contrib import admin
from transactions.models import CurrencyRate, WithholdingTax, ImportFile, TaxCalculation, TaxSummary, Transaction, BaseTransaction, AssetTransaction, DividendTransaction, WithholdingTaxTransaction

BASE_INFO = "Base info"
ASSET_INFO = "Asset info"
RELATIONS = "Relations"

class ImportFileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_at")



class DividendAdmin(admin.ModelAdmin):
    date_hierarchy = "received_at"
    list_display = (
        "asset_name",
        "value_per_share",
        "value",
        "value_pln",
        "currency",
        # "withholding_tax",
        "received_at",
    )
    list_filter = ("currency", "received_at")
    search_fields = ("asset_name",)
    ordering = ("-received_at", "asset_name", "value_per_share", "value", "value_pln")

class WithholdingTaxAdmin(admin.ModelAdmin):
    date_hierarchy = "paid_at"
    list_display = (
        "asset_name",
        "value",
        "value_pln",
        "currency",
        "paid_at",
    )
    list_filter = ("currency", "paid_at")
    search_fields = ("asset_name",)
    ordering = ("-paid_at", "asset_name", "value", "value_pln")


class TaxCalculationOpeningInline(admin.StackedInline):
    verbose_name_plural = "As Closing Tax Calculations"
    model = TaxCalculation
    fk_name = "closing_transaction"
    extra = 0


class TaxCalculationClosingInline(admin.StackedInline):
    verbose_name_plural = "As Opening Tax Calculations"
    model = TaxCalculation
    fk_name = "opening_transaction"
    extra = 0


class TransactionAdmin(admin.ModelAdmin):
    date_hierarchy = "executed_at"
    list_display = (
        "asset_name",
        "colored_side",
        "asset_type",
        "price",
        "quantity",
        "value",
        "value_pln",
        "currency",
        # "fee",
        "executed_at",
    )
    list_filter = ("side", "asset_type", "currency", "executed_at")
    search_fields = ("asset_name", "asset_type")
    ordering = ("-executed_at", "asset_name", "fee", "quantity", "value", "value_pln")
    inlines = [
        TaxCalculationOpeningInline,
        TaxCalculationClosingInline,
    ]


class AssetTransactionAdmin(admin.ModelAdmin):
    date_hierarchy = "executed_at"
    list_display = (
        "asset_name",
        "colored_side",
        "asset_type",
        "price",
        "quantity",
        "value",
        "value_pln",
        "currency",
        # "fee",
        "executed_at",
    )
    list_filter = ("side", "asset_type", "currency", "executed_at")
    search_fields = ("asset_name", "asset_type")
    ordering = ("-executed_at", "asset_name", "fee", "quantity", "value", "value_pln")

    fieldsets = (
        (
            BASE_INFO,
            {
                "fields": (
                    "report_file",
                    "previous_day_currency_rate",
                    "asset_name",
                    "asset_type",
                    "currency",
                    "executed_at",
                )
            },
        ),
        (
            ASSET_INFO,
            {
                "fields": (
                    "side",
                    "price",
                    "fee",
                    "quantity",
                    "value",
                    "full_value",
                    "value_pln",
                    "full_value_pln",
                    "raw_data",
                )
            },
        )
    )

class DividendTransactionAdmin(admin.ModelAdmin):
    date_hierarchy = "executed_at"
    list_display = (
        "asset_name",
        "value",
        "value_per_share",
        "value_pln",
        "currency",
        "withholding_tax_transaction",
        "executed_at",
    )
    list_filter = ("currency", "executed_at")
    search_fields = ("asset_name",)
    ordering = ("-executed_at", "asset_name", "value_per_share", "value", "value_pln")
    fieldsets = (
        (
            RELATIONS,
            {
                "fields": (
                    "report_file",
                    "previous_day_currency_rate",
                    "withholding_tax_transaction",
                )
            },
        ),
        (
            BASE_INFO,
            {
                "fields": (
                    # "report_file",
                    # "previous_day_currency_rate",
                    "asset_name",
                    "asset_type",
                    "currency",
                    "executed_at",
                )
            },
        ),
        (
            ASSET_INFO,
            {
                "fields": (
                    # "withholding_tax_transaction",
                    "value",
                    "value_per_share",
                    "value_pln",
                    "raw_data",
                )
            },
        )
    )

# NOTE add nested dividend model here? (inline)
class WithholdingTaxTransactionAdmin(admin.ModelAdmin):
    date_hierarchy = "executed_at"
    list_display = (
        "asset_name",
        "value",
        "value_pln",
        "currency",
        "executed_at",
    )
    list_filter = ("currency", "executed_at")
    search_fields = ("asset_name",)
    ordering = ("-executed_at", "asset_name", "value", "value_pln")
    fieldsets = (
        (
            "Relations",
            {
                "fields": (
                    "report_file",
                    "previous_day_currency_rate",
                )
            },
        ),
        (
            BASE_INFO,
            {
                "fields": (
                    # "report_file",
                    # "previous_day_currency_rate",
                    "asset_name",
                    "asset_type",
                    "currency",
                    "executed_at",
                )
            },
        ),
        (
            ASSET_INFO,
            {
                "fields": (
                    "value",
                    "value_pln",
                    "raw_data",
                )
            },
        )
    )

class TaxSummaryAdmin(admin.ModelAdmin):
    list_display = ("year", "tax_equity", "tax_dividend", "revenue_equity", "revenue_dividend", "cost_equity", "tax_paid_dividend")
    ordering = ("-year", "tax_equity", "tax_dividend", "revenue_equity", "revenue_dividend", "cost_equity", "tax_paid_dividend")


class TaxCalculationAdmin(admin.ModelAdmin):
    date_hierarchy = "closing_transaction__executed_at"
    list_display = (
        "id",
        "opening_transaction",
        "closing_transaction",
        "tax",
        "revenue",
        "cost",
        "profit_or_loss",
        "quantity",
    )
    list_filter = ("opening_transaction__asset_type", "closing_transaction__asset_type")
    search_fields = ("closing_transaction__asset_name", "opening_transaction__asset_name")
    ordering = ("-closing_transaction__executed_at", "tax", "revenue", "profit_or_loss", "cost")


class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ("date", "usd", "eur", "gbp", "chf")
    ordering = ("-date", "usd", "eur", "gbp", "chf")


admin.site.register(ImportFile, ImportFileAdmin)
# admin.site.register(Dividend, DividendAdmin)
admin.site.register(WithholdingTax, WithholdingTaxAdmin)
admin.site.register(Transaction, TransactionAdmin)
# admin.site.register(BaseTransaction, BaseTransactionAdmin)
admin.site.register(AssetTransaction, AssetTransactionAdmin)
admin.site.register(DividendTransaction, DividendTransactionAdmin)
admin.site.register(WithholdingTaxTransaction, WithholdingTaxTransactionAdmin)

admin.site.register(CurrencyRate, CurrencyRateAdmin)
admin.site.register(TaxSummary, TaxSummaryAdmin)
admin.site.register(TaxCalculation, TaxCalculationAdmin)
