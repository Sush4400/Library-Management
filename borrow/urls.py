from django.urls import path
from .views import *


urlpatterns = [
    path("", Borrow.as_view(), name="borrow")
]