
from django.http import HttpResponse
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# changed one more try
urlpatterns = [
    path('hello/', lambda request: HttpResponse('Hello Okey let"s change it!')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
