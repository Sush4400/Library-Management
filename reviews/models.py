from django.db import models
from books.models import Book
from core.utils import update_book_rating


# Create your models here.
class Review(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_book_rating(self.book)

    def delete(self, *args, **kwargs):
        book = self.book
        super().delete(*args, **kwargs)
        update_book_rating(book)

    class Meta:
        db_table = "reviews"
        unique_together = ("user", "book")
        indexes = [
            models.Index(fields=["book"]),
        ]