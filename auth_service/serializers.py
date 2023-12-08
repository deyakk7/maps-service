from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        depth = 1
        fields = ('id', 'email', 'username', 'profile')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active']
