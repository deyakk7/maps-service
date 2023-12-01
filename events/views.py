from datetime import datetime

from django.utils import timezone
from rest_framework import generics
from rest_framework import permissions

from .models import Event, Review
from .serializers import EventsSerializer, ReviewSerializer
from api.permissions import IsOwnerOrReadOnly


class EventsListView(generics.ListCreateAPIView):
    serializer_class = EventsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        Event.objects.filter(end_date__lt=datetime.now(timezone.utc)).delete()
        return Event.objects.all()


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
