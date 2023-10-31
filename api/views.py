from rest_framework import viewsets, authentication, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
