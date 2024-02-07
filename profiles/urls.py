from django.urls import path

from .views import ProfileList, ProfileDetail, PersonalProfileDetail

urlpatterns = [
    path('', ProfileList.as_view(), name='profile-list'),
    path('me/', PersonalProfileDetail.as_view(), name='profile-me'),
    path('<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
]
