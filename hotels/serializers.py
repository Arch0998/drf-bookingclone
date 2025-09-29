from rest_framework import serializers

from hotels.models import Hotel, Room, Location, RoomType, Amenity


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "country", "city"]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name", "description"]


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = [
            "id",
            "name",
            "description",
            "max_guests",
            "size",
            "bed_count",
        ]


class RoomSerializer(serializers.ModelSerializer):
    room_type = RoomTypeSerializer(read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "number",
            "room_type",
            "price",
            "is_available",
            "max_guests",
            "amenities",
            "photos",
        ]


class RoomShortSerializer(serializers.ModelSerializer):
    room_type_name = serializers.CharField(
        source="room_type.name", read_only=True
    )

    class Meta:
        model = Room
        fields = [
            "id",
            "number",
            "room_type_name",
            "price",
            "photos",
            "max_guests",
        ]


class HotelListSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    rooms_count = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            "id",
            "name",
            "description",
            "location",
            "address",
            "rating",
            "photos",
            "rooms_count",
            "min_price",
        ]

    def get_rooms_count(self, obj):
        return obj.rooms.filter(is_available=True).count()

    def get_min_price(self, obj):
        min_price = (
            obj.rooms.filter(is_available=True).order_by("price").first()
        )
        return min_price.price if min_price else None


class HotelCreateUpdateSerializer(serializers.ModelSerializer):
    location_data = serializers.DictField(write_only=True, required=False)

    class Meta:
        model = Hotel
        fields = [
            "id",
            "name",
            "description",
            "location",
            "address",
            "photos",
            "location_data",
        ]
        read_only_fields = ["id", "rating"]

    def create(self, validated_data):
        location_data = validated_data.pop("location_data", None)

        if location_data:
            location, created = Location.objects.get_or_create(
                country=location_data["country"], city=location_data["city"]
            )
            validated_data["location"] = location

        return super().create(validated_data)

    def update(self, instance, validated_data):
        location_data = validated_data.pop("location_data", None)

        if location_data:
            location, created = Location.objects.get_or_create(
                country=location_data["country"], city=location_data["city"]
            )
            validated_data["location"] = location

        return super().update(instance, validated_data)


class HotelDetailSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    rooms = RoomShortSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source="owner.username", read_only=True)
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = [
            "id",
            "name",
            "description",
            "location",
            "address",
            "rating",
            "photos",
            "rooms",
            "owner_name",
            "reviews_count",
        ]

    def get_reviews_count(self, obj):
        return obj.reviews.count()


class RoomCreateUpdateSerializer(serializers.ModelSerializer):
    room_type_id = serializers.IntegerField(write_only=True, required=False)
    amenities_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Room
        fields = [
            "id",
            "number",
            "room_type",
            "room_type_id",
            "price",
            "is_available",
            "max_guests",
            "amenities",
            "amenities_ids",
            "photos",
        ]
        read_only_fields = ["id", "hotel", "room_type"]

    def create(self, validated_data):
        room_type_id = validated_data.pop("room_type_id", None)
        amenities_ids = validated_data.pop("amenities_ids", [])

        if room_type_id:
            try:
                room_type = RoomType.objects.get(id=room_type_id)
                validated_data["room_type"] = room_type
            except RoomType.DoesNotExist:
                raise serializers.ValidationError("Invalid room type ID")

        room = super().create(validated_data)

        if amenities_ids:
            amenities = Amenity.objects.filter(id__in=amenities_ids)
            room.amenities.set(amenities)

        return room

    def update(self, instance, validated_data):
        room_type_id = validated_data.pop("room_type_id", None)
        amenities_ids = validated_data.pop("amenities_ids", None)

        if room_type_id:
            try:
                room_type = RoomType.objects.get(id=room_type_id)
                validated_data["room_type"] = room_type
            except RoomType.DoesNotExist:
                raise serializers.ValidationError("Invalid room type ID")

        room = super().update(instance, validated_data)

        if amenities_ids is not None:
            amenities = Amenity.objects.filter(id__in=amenities_ids)
            room.amenities.set(amenities)

        return room
