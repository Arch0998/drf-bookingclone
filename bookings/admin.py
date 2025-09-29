from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "room",
        "check_in",
        "check_out",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at", "room")
    search_fields = ("user__username", "room__number", "room__hotel__name")
    autocomplete_fields = ("user", "room")


# Register your models here.
