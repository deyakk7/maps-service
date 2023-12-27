from datetime import datetime

from django.utils import timezone
from rest_framework import generics
from rest_framework import permissions

from api.permissions import IsOwnerOrReadOnly
from .models import Event, Review
from .serializers import EventsSerializer, ReviewSerializer


class EventsListView(generics.ListCreateAPIView):
    serializer_class = EventsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        expired_events = Event.objects.filter(end_date__lt=datetime.now(timezone.utc))
        expired_events.update(is_expired=True)
        return Event.objects.filter(is_expired=False)


class EventsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventsSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class EventsForCurrentUserList(generics.ListAPIView):
    serializer_class = EventsSerializer
    permissions = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)


class ReviewsListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)
