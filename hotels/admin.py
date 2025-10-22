from django.contrib import admin

from hotels.models import Hotel, Location, Room, RoomType, Amenity


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["city", "country"]
    list_filter = ["country"]
    search_fields = ["city", "country"]


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "max_guests", "size", "bed_count"]
    search_fields = ["name"]


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


class RoomInline(admin.TabularInline):
    model = Room
    extra = 0
    fields = ["number", "room_type", "price", "is_available", "max_guests"]


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "location", "rating", "rooms_count"]
    list_filter = ["location__country", "location__city", "rating"]
    search_fields = ["name", "description"]
    readonly_fields = ["rating"]
    inlines = [RoomInline]

    def rooms_count(self, obj):
        return obj.rooms.count()

    rooms_count.short_description = "Rooms"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "hotel",
        "number",
        "room_type",
        "price",
        "is_available",
        "max_guests",
    ]
    list_filter = ["hotel", "room_type", "is_available"]
    search_fields = ["hotel__name", "number"]
    filter_horizontal = ["amenities"]
