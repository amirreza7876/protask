from django.urls import path
from .views import RegisterApi, user_detail

urlpatterns = [
    path('api/register/', RegisterApi.as_view()),
    path('my_data/', user_detail)
]
