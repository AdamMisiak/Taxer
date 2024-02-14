from django.contrib import admin
from utils.models import Broker


class BrokerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")

admin.site.register(Broker, BrokerAdmin)
