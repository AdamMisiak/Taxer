from django.contrib import admin
from tax_calculations.models import AssetTaxCalculation

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
        "tax",
        "revenue",
        "cost",
        "profit_or_loss",
        "quantity",
    )
    list_filter = ("opening_transaction__asset_type", "closing_transaction__asset_type")
    search_fields = ("closing_transaction__asset_name", "opening_transaction__asset_name")
    ordering = ("-closing_transaction__executed_at", "tax", "revenue", "profit_or_loss", "cost")

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

admin.site.register(AssetTaxCalculation, AssetTaxCalculationAdmin)