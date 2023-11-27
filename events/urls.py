from django.urls import path

from .views import (EventsListView, EventsDetailView,
                    ReviewListView, ReviewDetailView)


urlpatterns = [
    path('', EventsListView.as_view(), name='events-list'),
    path('<int:pk>/', EventsDetailView.as_view(), name='events-detail'),
    path('reviews/', ReviewListView.as_view(), name='reviews-list'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='reviews-detail'),
]
