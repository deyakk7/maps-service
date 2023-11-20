from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

from auth_service.models import Profile

User = get_user_model()

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        depth = 1