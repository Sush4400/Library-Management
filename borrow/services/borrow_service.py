from django.db import transaction
from django.utils import timezone
from datetime import timedelta

from ..models import Borrow
from books.models import BookCopy

MAX_BORROW_LIMIT = 5
BORROW_DAYS = 14


class BorrowService:
    @staticmethod
    @transaction.atomic
    def borrow_book(user, book_id):
        # check active borrows
        active_borrows = Borrow.objects.filter(
            user=user, is_returned=False
        ).count()
        
        if active_borrows >= MAX_BORROW_LIMIT:
            raise Exception("Borrow Limit Reached!")
        
        # lock available book copy
        book_copy = BookCopy.objects.select_for_update().filter(
            book=book_id, is_available=True
        ).first()

        if not book_copy:
            raise Exception("No Available Copies!")
        
        # mark available
        book_copy.status = "BORROWED"
        book_copy.save()

        borrow = Borrow.objects.create(
            user=user,
            book_copy=book_copy,
            due_date=timezone.now()+timedelta(days=BORROW_DAYS)
        )

        return borrow
