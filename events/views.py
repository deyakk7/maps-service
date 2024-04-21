from datetime import datetime

from django.http import JsonResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsOwnerOrReadOnly
from .filters import EventMyFilter
from .models import Event, Review
from .serializers import EventsSerializer, ReviewSerializer


class EventsListView(generics.ListCreateAPIView):
    serializer_class = EventsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Event.objects.all()

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventMyFilter

    def get_queryset(self):
        queryset = Event.objects.filter(user=self.request.user)
        filtered_queryset = EventMyFilter(self.request.GET, queryset=queryset).qs.order_by('-created_at')
        return filtered_queryset


class ReviewsListView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, event_id=self.kwargs['pk'])

    def get_queryset(self):
        return Review.objects.filter(event_id=self.kwargs['pk'])


class ReviewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)
