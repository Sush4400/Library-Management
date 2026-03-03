from django.urls import path
from .views import *


urlpatterns = [
    path("", Reviews.as_view(), name="reviews")
]