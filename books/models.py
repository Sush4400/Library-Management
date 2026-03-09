from django.db import models


# Create your models here.
class Author(models.Model):
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
    name = models.CharField(max_length=50, blank=False)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    email = models.EmailField(blank=False)
    phone = models.CharField(max_length=10, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "publishers"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "categories"
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ["name"]


class Book(models.Model):
    title = models.CharField(max_length=100, unique=True, null=False)
    authors = models.ManyToManyField(Author, related_name="books")
    publisher = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name="books")
    categories = models.ManyToManyField(Category, related_name="books")
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
        verbose_name_plural = "Book Copies"
