from rest_framework import serializers

from hotels.models import Hotel, Room


class RoomShortSerializer(serializers.ModelSerializer):
    room_type = serializers.StringRelatedField()
    
    class Meta:
        model = Room
        fields = ["number", "room_type", "price", "photos"]


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ["id",
                  "name",
                  "description",
                  "location",
                  "address",
                  "rating",
                  "photos"
                  ]
    
    def validate_photos(self, value):
        if not value:
            raise serializers.ValidationError("Photo required for hotel.")
        return value


class HotelDetailSerializer(serializers.ModelSerializer):
    rooms = RoomShortSerializer(many=True, read_only=True)
    
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
        ]
