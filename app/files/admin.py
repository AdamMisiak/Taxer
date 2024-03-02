from django.contrib import admin
from files.models import ReportFile


class ReportFileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "user", "created_at")
    readonly_fields=('user',)

    def save_model(self, request, instance, form, change):
        user = request.user 
        instance = form.save(commit=False)
        if not change or not instance.user:
            instance.user = user
        instance.user = user
        instance.save()
        return instance

admin.site.register(ReportFile, ReportFileAdmin)
