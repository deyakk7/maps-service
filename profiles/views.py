from rest_framework import generics, permissions

from .models import Profile
from .serializers import ProfileSerializer
from api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, *args, **kwargs):
        user = self.get_object().user
        user.delete()
        super().delete(request, *args, **kwargs)
