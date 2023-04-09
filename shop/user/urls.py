from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import LoginAPIView, RegistrAPIView

urlpatterns = [
    path('login', LoginAPIView.as_view()),
    path('registr', RegistrAPIView.as_view())
]