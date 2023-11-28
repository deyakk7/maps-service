from rest_framework import serializers

from .models import Event, Review


class EventsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    reviews = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'
        depth = 1
        read_only_fields = ['id', 'user', 'rating', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
