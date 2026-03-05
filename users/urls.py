from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *


urlpatterns = [
    path("", UsersView.as_view(), name="users"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("logout/", LogoutView.as_view(), name="logout")
]
