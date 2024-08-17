from django.contrib import admin
from tax_summaries.models import AsssetTaxSummary

BASE_INFO = "Base info"
OTHER_INFO = "Other info"
ASSET_INFO = "Asset info"
RELATIONS = "Relations"

class AsssetTaxSummaryAdmin(admin.ModelAdmin):
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

    

admin.site.register(AsssetTaxSummary, AsssetTaxSummaryAdmin)

