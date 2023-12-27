from django.urls import path

from .views import (EventsListView, EventsDetailView,
                    ReviewsListView, ReviewsDetailView,
                    EventsForCurrentUserList)

urlpatterns = [
    path('', EventsListView.as_view(), name='events-list'),
    path('my/', EventsForCurrentUserList.as_view(), name='events-for-user'),
    path('<int:pk>/', EventsDetailView.as_view(), name='events-detail'),
    path('reviews/', ReviewsListView.as_view(), name='reviews-list'),
    path('reviews/<int:pk>/', ReviewsDetailView.as_view(), name='reviews-detail'),
]
