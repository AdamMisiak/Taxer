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
        "tax",
    )
    list_filter = ("year",)
    search_fields = ("year",)
    ordering = ("-year", "tax", "revenue", "cost", "tax")

    fieldsets = (
        (
            BASE_INFO,
            {
                "fields": (
                    "year",
                    "cost",
                    "revenue",
                    "tax",
                )
            },
        ),
    )

    

admin.site.register(AsssetTaxSummary, AsssetTaxSummaryAdmin)

