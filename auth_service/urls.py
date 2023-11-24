from django.urls import path, include, re_path
from rest_framework import routers

from .views import UserViewSet, ProfileViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
] + router.urls
