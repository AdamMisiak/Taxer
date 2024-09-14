from django.contrib import admin
from tax_summaries.models import GeneralTaxSummary, AssetTaxSummary, OptionTaxSummary, DividendTaxSummary
from tax_calculations.models import AssetTaxCalculation, OptionTaxCalculation, DividendTaxCalculation

BASE_INFO = "Base info"
OTHER_INFO = "Other info"
ASSET_INFO = "Asset info"
RELATIONS = "Relations"


class AssetTaxCalculationInline(admin.StackedInline):
    verbose_name_plural = "Related Asset Tax Calculation"
    model = AssetTaxCalculation
    fk_name = "tax_summary"
    extra = 0

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
    inlines = [
        AssetTaxCalculationInline,
    ]

    fieldsets = (
        (
            RELATIONS,
            {
                "fields": (
                    "general_tax_summary",
                )
            },
        ),
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

class GeneralTaxSummaryAdmin(admin.ModelAdmin):
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


class OptionTaxCalculationInline(admin.StackedInline):
    verbose_name_plural = "Related Option Tax Calculation"
    model = OptionTaxCalculation
    fk_name = "tax_summary"
    extra = 0

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
    # inlines = [
    #     OptionTaxCalculationInline,
    # ]

    fieldsets = (
        (
            RELATIONS,
            {
                "fields": (
                    "general_tax_summary",
                )
            },
        ),
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

class DividendTaxCalculationInline(admin.StackedInline):
    verbose_name_plural = "Related Dividend Tax Calculation"
    model = DividendTaxCalculation
    fk_name = "tax_summary"
    extra = 0
    
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
    inlines = [
        DividendTaxCalculationInline,
    ]

    fieldsets = (
        (
            RELATIONS,
            {
                "fields": (
                    "general_tax_summary",
                )
            },
        ),
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
admin.site.register(GeneralTaxSummary, GeneralTaxSummaryAdmin)
admin.site.register(OptionTaxSummary, OptionTaxSummaryAdmin)
admin.site.register(DividendTaxSummary, DividendTaxSummaryAdmin)

