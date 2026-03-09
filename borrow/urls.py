from django.urls import path
from .views import *


urlpatterns = [
    path("", BorrowBookView.as_view(), name="borrow_book"),
    path("return/", BorrowBookView.as_view(), name="borrow_book"),
]