from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "booking",
        "amount",
        "status",
        "payment_type",
        "paid_at",
    )
    list_filter = ("status", "payment_type", "paid_at")
    search_fields = ("booking__user__username", "booking__room__hotel__name")
    autocomplete_fields = ("booking",)
