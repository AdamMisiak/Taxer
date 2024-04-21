from django.contrib import admin
from tax_calculations.models import AssetTaxCalculation

# class AssetTaxCalculationAdmin(admin.ModelAdmin):
#     date_hierarchy = "closing_transaction__executed_at"
#     list_display = (
#         "id",
#         "opening_transaction",
#         "closing_transaction",
#         "tax",
#         "revenue",
#         "cost",
#         "profit_or_loss",
#         "quantity",
#     )
#     list_filter = ("opening_transaction__asset_type", "closing_transaction__asset_type")
#     search_fields = ("closing_transaction__asset_name", "opening_transaction__asset_name")
#     ordering = ("-closing_transaction__executed_at", "tax", "revenue", "profit_or_loss", "cost")

# admin.site.register(AssetTaxCalculation, AssetTaxCalculationAdmin)
