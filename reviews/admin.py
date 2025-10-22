from django.contrib import admin
from django.utils.html import format_html

from reviews.models import Review


def photo_preview(obj):
    if obj.photos:
        return format_html('<img src="{}" width="60" />', obj.photos.url)
    return "-"


photo_preview.short_description = "Photo"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "hotel",
        "user",
        "rating",
        "comment",
        "created_at",
        photo_preview,
    )
    list_filter = ("hotel", "rating", "created_at")
    search_fields = ("user__username", "hotel__name", "comment")
    autocomplete_fields = ("hotel", "user")
