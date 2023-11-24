from django.urls import path
from .views import EventsListView, EventsDetailView

from rest_framework import routers


urlpatterns = [
    path('', EventsListView.as_view(), name='events-list'),
    path('<int:pk>/', EventsDetailView.as_view(), name='events-detail'),
] 
