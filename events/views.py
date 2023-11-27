from rest_framework import generics
from rest_framework import permissions

from .models import Event, Review
from .serializers import EventsSerializer, ReviewSerializer
from api.permissions import IsOwnerOrReadOnly


class EventsListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)
