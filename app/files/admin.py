from django.contrib import admin
from files.models import ReportFile


class ReportFileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "created_at")

admin.site.register(ReportFile, ReportFileAdmin)
