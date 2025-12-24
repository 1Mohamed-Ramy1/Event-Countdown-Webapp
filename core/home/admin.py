from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "uid", "event_date", "created_at")
    readonly_fields = ("uid", "created_at")
    search_fields = ("name",)
