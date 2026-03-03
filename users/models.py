from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        LIBRARIAN = "LIBRARIAN", "Librarian"
        MEMBER = "MEMBER", "Member"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usename = None
    email = models.EmailField(unique=True, blank=False)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return self.email
