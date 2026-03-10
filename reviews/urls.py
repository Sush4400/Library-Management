from django.urls import path
from .views import *


urlpatterns = [
    path("", ReviewAPIView.as_view()),
    path("<int:id>/", ReviewRetrieveUpdateDestroyAPIView.as_view())
]