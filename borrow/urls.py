from django.urls import path
from .views import *


urlpatterns = [
    path("", BorrowBookView.as_view(), name="borrow_book"),
    path("return/", ReturnBookView.as_view(), name="borrow_book"),
    path("history/", BorrowHistoryView.as_view(), name="borrow_book"),
    path("history/<int:user_id>/", UserBorrowedBooksView.as_view(), name="borrow_book"),
]