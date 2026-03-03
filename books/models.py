from django.db import models
import uuid


# Create your models here.
class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False, db_index=True)
    dob = models.DateField()
    nationality = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "authors"
        ordering = ["name"]

    def __str__(self):
        return self.name
    

class Publisher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=10, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_name = "publishers"

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Mets:
        db_table = "categories"
        ordering = ["name"]


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True, null=False)
    authors = models.ManyToManyField(Author, related_name="books")
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name="books")
    category = models.ManyToManyField(Category, related_name="books")
    description= models.TextField(blank=True)
    publication_date = models.DateField()
    edition = models.CharField(max_length=50, blank=True)
    language = models.CharField(max_length=50, default="English")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_copies = models.PositiveIntegerField(default=0)
    available_copies = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "books"
    
    def __str__(self):
        return self.title


class BookCopy(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABEL", "Available"
        BORROWED = "BORROWED", "Borrowed"
        LOST = "LOST", "Lost"
        DAMAGED = "DAMAGED", "Damaged"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")
    barcode =  models.CharField(max_length=50, blank=True)
    shelf_location = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title}[{self.barcode}]"

    class Meta:
        db_table = "book_copies"
        indexes = [
            models.Index(fields=["barcode"]),
            models.Index(fields=["status"])
        ]
