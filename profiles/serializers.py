from rest_framework.serializers import ModelSerializer

from auth_service.serializers import UserSerializer
from .models import Profile


class ProfileSerializer(ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')