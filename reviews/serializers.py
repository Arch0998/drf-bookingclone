from rest_framework import serializers

from hotels.models import Hotel
from reviews.models import Review
from users.models import User


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class HotelShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ["id", "name"]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    hotel = HotelShortSerializer(read_only=True)
    hotel_id = serializers.PrimaryKeyRelatedField(
        queryset=Hotel.objects.all(), write_only=True, source="hotel"
    )
    
    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "hotel",
            "hotel_id",
            "rating",
            "comment",
            "photos",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "user", "hotel"]
    
    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 - 5.")
        return value
    
    def validate(self, attrs):
        user = self.context["request"].user
        hotel = attrs.get("hotel")
        if self.instance is None and Review.objects.filter(
                user=user, hotel=hotel
        ).exists():
            raise serializers.ValidationError(
                "You have already reviewed this hotel."
            )
        return attrs
    
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
