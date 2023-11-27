from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('auth/', include('auth_service.urls')),
    path('profiles/', include('profiles.urls')),
] 
