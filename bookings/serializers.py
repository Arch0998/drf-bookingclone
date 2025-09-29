from rest_framework import serializers

from bookings.models import Booking
from hotels.models import Room
from hotels.serializers import RoomShortSerializer
from users.models import User


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class BookingSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    room = RoomShortSerializer(read_only=True)
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), write_only=True, source="room"
    )
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "room",
            "room_id",
            "check_in",
            "check_out",
            "created_at",
            "total_price",
            "status",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "user",
            "room",
            "total_price",
            "status",
        ]

    def get_total_price(self, obj):
        if obj.check_in and obj.check_out and obj.room:
            days = (obj.check_out - obj.check_in).days
            return days * obj.room.price
        return None

    def validate(self, attrs):
        check_in = attrs.get("check_in")
        check_out = attrs.get("check_out")
        room = attrs.get("room")
        if check_in and check_out and check_in >= check_out:
            raise serializers.ValidationError(
                {"check_out": "The check-out must be later than the check-in."}
            )
        if room and check_in and check_out:
            overlapping = Booking.objects.filter(
                room=room, check_in__lt=check_out, check_out__gt=check_in
            )
            if self.instance:
                overlapping = overlapping.exclude(pk=self.instance.pk)
            if overlapping.exists():
                raise serializers.ValidationError(
                    "This room is already booked for the selected dates."
                )
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)
