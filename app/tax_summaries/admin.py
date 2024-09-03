from django.contrib import admin
from tax_summaries.models import AssetTaxSummary, OptionTaxSummary, DividendTaxSummary

BASE_INFO = "Base info"
OTHER_INFO = "Other info"
ASSET_INFO = "Asset info"
RELATIONS = "Relations"

class AssetTaxSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "year",
        "revenue",
        "cost",
        "profit_or_loss",
        "tax",
    )
    list_filter = ("year",)
    search_fields = ("year",)
    ordering = ("-year", "revenue", "cost", "profit_or_loss", "tax")

    fieldsets = (
        (
            BASE_INFO,
            {
                "fields": (
                    "year",
                    "cost",
                    "revenue",
                    "profit_or_loss",
                    "tax",
                )
            },
        ),
    )

class OptionTaxSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "year",
        "revenue",
        "cost",
        "profit_or_loss",
        "tax",
    )
    list_filter = ("year",)
    search_fields = ("year",)
    ordering = ("-year", "revenue", "cost", "profit_or_loss", "tax")

    fieldsets = (
        (
            BASE_INFO,
            {
                "fields": (
                    "year",
                    "cost",
                    "revenue",
                    "profit_or_loss",
                    "tax",
                )
            },
        ),
    )

class DividendTaxSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "year",
        "revenue",
        "tax_paid",
        "tax",
    )
    list_filter = ("year",)
    search_fields = ("year",)
    ordering = ("-year", "revenue", "tax_paid", "tax")

    fieldsets = (
        (
            BASE_INFO,
            {
                "fields": (
                    "year",
                    "tax_paid",
                    "revenue",
                    "tax",
                )
            },
        ),
    )

admin.site.register(AssetTaxSummary, AssetTaxSummaryAdmin)
admin.site.register(OptionTaxSummary, OptionTaxSummaryAdmin)
admin.site.register(DividendTaxSummary, DividendTaxSummaryAdmin)

