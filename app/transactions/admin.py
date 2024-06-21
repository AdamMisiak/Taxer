from django.contrib import admin
from transactions.models import CurrencyRate, WithholdingTax, ImportFile, InterestRateTransaction, TaxCalculation, TaxSummary, Transaction, OptionTransaction, BaseTransaction, AssetTransaction, DividendTransaction, WithholdingTaxTransaction
from tax_calculations.models import AssetTaxCalculation, OptionTaxCalculation

BASE_INFO = "Base info"
OTHER_INFO = "Other info"
ASSET_INFO = "Asset info"
DIVIDEND_INFO = "Dividend info"
WITHHOLDING_TAX_INFO = "Withholding tax info"
OPTION_INFO = "Option info"
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

class AssetTaxCalculationOpeningInline(admin.StackedInline):
    verbose_name_plural = "As Closing Tax Calculations"
    model = AssetTaxCalculation
    fk_name = "closing_transaction"
    extra = 0


class AssetTaxCalculationClosingInline(admin.StackedInline):
    verbose_name_plural = "As Opening Tax Calculations"
    model = AssetTaxCalculation
    fk_name = "opening_transaction"
    extra = 0

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
    inlines = [
        AssetTaxCalculationOpeningInline,
        AssetTaxCalculationClosingInline,
    ]

    fieldsets = (
        (
            RELATIONS,
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

class OptionTaxCalculationOpeningInline(admin.StackedInline):
    verbose_name_plural = "As Closing Tax Calculations"
    model = OptionTaxCalculation
    fk_name = "closing_transaction"
    extra = 0


class OptionTaxCalculationClosingInline(admin.StackedInline):
    verbose_name_plural = "As Opening Tax Calculations"
    model = OptionTaxCalculation
    fk_name = "opening_transaction"
    extra = 0

class OptionTransactionAdmin(admin.ModelAdmin):
    date_hierarchy = "executed_at"
    list_display = (
        "asset_name",
        "colored_side",
        "expired",
        "asset_type",
        "option_type",
        "price",
        "strike_price",
        "quantity",
        "value",
        "value_pln",
        "currency",
        # "fee",
        "executed_at",
    )
    list_filter = ("side", "asset_type", "option_type", "currency", "executed_at")
    search_fields = ("asset_name", "asset_type", "option_type")
    ordering = ("-executed_at", "asset_name", "fee", "quantity", "value", "value_pln")
    inlines = [
        OptionTaxCalculationOpeningInline,
        OptionTaxCalculationClosingInline,
    ]

    fieldsets = (
        (
            RELATIONS,
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
                    "asset_name",
                    "asset_type",
                    "currency",
                    "executed_at",
                    "raw_data",
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
                )
            },
        ),
        (
            OPTION_INFO,
            {
                "fields": (
                    "base_instrument",
                    "strike_price",
                    "option_type",
                    "expired",
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
                    "asset_name",
                    "asset_type",
                    "currency",
                    "executed_at",
                    "raw_data",
                )
            },
        ),
        (
            DIVIDEND_INFO,
            {
                "fields": (
                    "value",
                    "value_per_share",
                    "value_pln",
                )
            },
        )
    )

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
            RELATIONS,
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
                    "asset_name",
                    "asset_type",
                    "currency",
                    "executed_at",
                    "raw_data",
                )
            },
        ),
        (
            WITHHOLDING_TAX_INFO,
            {
                "fields": (
                    "value",
                    "value_pln",
                )
            },
        )
    )


class InterestRateTransactionAdmin(admin.ModelAdmin):
    date_hierarchy = "executed_at"
    list_display = (
        "asset_name",
        "colored_side",
        "asset_type",
        "value",
        "value_pln",
        "currency",
        "executed_at",
    )
    list_filter = ("side", "currency", "executed_at")
    search_fields = ("asset_name", "asset_type")
    ordering = ("-executed_at", "asset_name", "value", "value_pln")

    fieldsets = (
        (
            RELATIONS,
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
                    "asset_name",
                    "asset_type",
                    "currency",
                    "executed_at",
                    "raw_data",
                )
            },
        ),
        (
            OTHER_INFO,
            {
                "fields": (
                    "side",
                    "value",
                    "value_pln",
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
admin.site.register(OptionTransaction, OptionTransactionAdmin)
admin.site.register(DividendTransaction, DividendTransactionAdmin)
admin.site.register(WithholdingTaxTransaction, WithholdingTaxTransactionAdmin)
admin.site.register(InterestRateTransaction, InterestRateTransactionAdmin)

admin.site.register(CurrencyRate, CurrencyRateAdmin)
admin.site.register(TaxSummary, TaxSummaryAdmin)
admin.site.register(TaxCalculation, TaxCalculationAdmin)
