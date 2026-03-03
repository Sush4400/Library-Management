from django.urls import path
from .views import *


urlpatterns = [
    path("", Books.as_view(), name="books")
]
