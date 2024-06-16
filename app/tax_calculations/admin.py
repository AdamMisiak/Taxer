from django.contrib import admin
from tax_calculations.models import AssetTaxCalculation, DividendTaxCalculation, OptionTaxCalculation

BASE_INFO = "Base info"
OTHER_INFO = "Other info"
ASSET_INFO = "Asset info"
RELATIONS = "Relations"

class AssetTaxCalculationAdmin(admin.ModelAdmin):
    date_hierarchy = "closing_transaction__executed_at"
    list_display = (
        "id",
        "opening_transaction",
        "closing_transaction",
        "colored_tax",
        "revenue",
        "cost",
        "profit_or_loss",
        "quantity",
    )
    list_filter = ("opening_transaction__asset_type", "closing_transaction__asset_type")
    search_fields = ("closing_transaction__asset_name", "opening_transaction__asset_name")
    ordering = ("-closing_transaction__executed_at", "-opening_transaction__executed_at", "tax", "revenue", "profit_or_loss", "cost")

    fieldsets = (
        (
            RELATIONS,
            {
                "fields": (
                    "opening_transaction",
                    "closing_transaction",
                )
            },
        ),
        (
            BASE_INFO,
            {
                "fields": (
                    "cost",
                    "revenue",
                    "profit_or_loss",
                    "tax_rate",
                    "tax",
                )
            },
        ),
        (
            OTHER_INFO,
            {
                "fields": (
                    "quantity",
                )
            },
        )
    )

class DividendTaxCalculationAdmin(admin.ModelAdmin):
    date_hierarchy = "dividend_transaction__executed_at"
    list_display = (
        "id",
        "withholding_tax_transaction",
        "dividend_transaction",
        "colored_tax",
        "revenue",
        "cost",
        "profit_or_loss",
    )
    list_filter = ("withholding_tax_transaction__asset_type", "dividend_transaction__asset_type")
    search_fields = ("dividend_transaction__asset_name", "withholding_tax_transaction__asset_name")
    ordering = ("-dividend_transaction__executed_at", "-withholding_tax_transaction__executed_at", "tax", "revenue", "profit_or_loss", "cost")

    fieldsets = (
        (
            RELATIONS,
            {
                "fields": (
                    "withholding_tax_transaction",
                    "dividend_transaction",
                )
            },
        ),
        (
            BASE_INFO,
            {
                "fields": (
                    "cost",
                    "revenue",
                    "profit_or_loss",
                    "tax_rate",
                    "tax",
                )
            },
        )
    )

class OptionTaxCalculationAdmin(admin.ModelAdmin):
    date_hierarchy = "closing_transaction__executed_at"
    list_display = (
        "id",
        "opening_transaction",
        "closing_transaction",
        "colored_tax",
        "revenue",
        "cost",
        "profit_or_loss",
    )
    list_filter = ("opening_transaction__asset_type", "closing_transaction__asset_type")
    search_fields = ("closing_transaction__asset_name", "opening_transaction__asset_name")
    ordering = ("-closing_transaction__executed_at", "-opening_transaction__executed_at", "tax", "revenue", "profit_or_loss", "cost")

    fieldsets = (
        (
            RELATIONS,
            {
                "fields": (
                    "opening_transaction",
                    "closing_transaction",
                )
            },
        ),
        (
            BASE_INFO,
            {
                "fields": (
                    "cost",
                    "revenue",
                    "profit_or_loss",
                    "tax_rate",
                    "tax",
                )
            },
        ),
    )

admin.site.register(AssetTaxCalculation, AssetTaxCalculationAdmin)
admin.site.register(DividendTaxCalculation, DividendTaxCalculationAdmin)
admin.site.register(OptionTaxCalculation, OptionTaxCalculationAdmin)
