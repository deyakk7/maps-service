from rest_framework import serializers
from .models import Event


class EventsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Event
        fields = '__all__'

