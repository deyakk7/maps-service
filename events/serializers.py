from rest_framework import serializers

from .models import Event, Review


class EventsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    profile = serializers.ReadOnlyField(source='user.profile.id')

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'image', 'created_at', 'updated_at',
                  'position_x', 'position_y', 'is_expired', 'total_reviews', 'user', 'rating', 'profile']
        depth = 1
        read_only_fields = ['id', 'user', 'rating', 'created_at', 'updated_at', 'reviews', 'total_reviews', 'profile']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    profile = serializers.ReadOnlyField(source='user.profile.id')

    class Meta:
        model = Review
        exclude = ['event']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'event', 'profile']
