from django.urls import path
from user.views import RegisterApi

urlpatterns = [
    path('api/register/', RegisterApi.as_view()),
]
