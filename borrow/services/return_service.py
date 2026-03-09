from django.utils import timezone
from django.db import transaction

from ..models import Borrow

FINE_PER_DAY = 10



class ReturnService:

    @staticmethod
    @transaction.atomic
    def return_book(borrow_id):
        borrow = Borrow.objects.select_related("book_copy").get(id=borrow_id)
        if borrow.is_returned:
            raise Exception("Book Already Returned!")
        
        borrow.return_date = timezone.now()
        borrow.is_returned = True

        if borrow.return_date > borrow.due_date:
            days_late = borrow.return_date - borrow.due_date
            borrow.fine_amount = days_late * FINE_PER_DAY

        borrow.save()

        # make copy available
        copy = borrow.book_copy
        copy.status = "AVAILABLE"
        copy.save()

        return borrow