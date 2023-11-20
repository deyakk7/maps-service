from rest_framework import viewsets, authentication, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, ProfileSerializer

from auth_service.models import Profile

User = get_user_model()
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]