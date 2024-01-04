from transactions.models import ImportFile, Transaction
from django.contrib import admin


class ImportFileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_at")
    # list_filter = ("author", "source")
    # search_fields = ("search_text", "author")
    # ordering = ("-created_at", "search_text", "author")


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("asset", "side", "asset_type", "price", "quantity", "value", "currency", "fee", "datetime")
    list_filter = ("asset", "side", "asset_type", "currency")
    search_fields = ("asset", "asset_type")
    ordering = ("-datetime", "asset", "fee", "quantity", "value")

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(ImportFile, ImportFileAdmin)