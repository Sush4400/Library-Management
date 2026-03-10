from .models import Review
from rest_framework import serializers
from books.models import Book
from books.serializers import BookListSerializer



class ReviewSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True
    )

    book_details = BookListSerializer(source="book", read_only=True)
    class Meta:
        model = Review
        fields = ["user", "rating", "book", "book_details", "comment"]
