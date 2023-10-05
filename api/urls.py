
from django.http import HttpResponse
from django.urls import path

urlpatterns = [
    path('hello/', lambda request: HttpResponse('Hello World!'))

]
