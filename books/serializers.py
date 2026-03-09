from rest_framework import serializers
from .models import Author, Category, Book, BookCopy, Publisher


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = [
            "id",
            "name",
            "dob",
            "nationality",
            "is_active"
        ]
        read_only_fields = ["id"]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "description", "is_active"]
        read_only_fields = ["id"]


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = ["id", "name", "address", "email", "phone", "website", "created_at"]
        read_only_fields = ["id"]


class BookWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ["title", "authors", "publisher", "categories", "description", "publication_date",
                  "edition", "language", "price", "total_copies", "available_copies"]

    def validate(self, data):
            total = data.get("total_copies")
            available = data.get("available_copies")

            if available is not None and total is not None and available > total:
                raise serializers.ValidationError(
                    "available_copies can't exceed total_copies"
                )
            return data


class BookListSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "authors", "publisher", "categories", "description", "publication_date",
                  "edition", "language", "price", "total_copies", "available_copies", "average_rating", "is_active"]
        

class BookCopySerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    class Meta:
        model = BookCopy
        fields = ["id", "book", "barcode", "shelf_location", "status"]
        read_only_fields = ["id"]
