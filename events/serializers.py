from rest_framework import serializers

from .models import Event, Review


class EventsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'image', 'created_at', 'updated_at', 'is_active', 'position_x', 'position_y', 'user', 'rating', 'reviews']
        depth = 1
        read_only_fields = ['id', 'user', 'rating', 'created_at', 'updated_at', 'reviews']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
