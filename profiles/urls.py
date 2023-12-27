from django.urls import path

from .views import ProfileList, ProfileDetail, PersonalProfileDetail

urlpatterns = [
    path('', ProfileList.as_view()),
    path('me/', PersonalProfileDetail.as_view()),
    path('<int:pk>/', ProfileDetail.as_view()),
]
