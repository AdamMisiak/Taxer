from transactions.models import ImportFile
from django.contrib import admin


class ImportFileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_at")
    # list_filter = ("author", "source")
    # search_fields = ("search_text", "author")
    # ordering = ("-created_at", "search_text", "author")


admin.site.register(ImportFile, ImportFileAdmin)