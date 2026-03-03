from django.db import models
import uuid
from books.models import BookCopy


# Create your models here.
class Borrow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="borrowed_books")
    book_copy = models.ForeignKey(BookCopy, on_delete=models.PROTECT, related_name="borrows")
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_returned = models.BooleanField(default=False)

    class Meta:
        db_table = "borrows"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["due_date"]),
            models.Index(fields=["is_returned"]),
        ]