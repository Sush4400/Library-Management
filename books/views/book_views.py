from rest_framework.permissions import IsAuthenticated
from ..models import *
from django.db import transaction
from core.permissions import RolePermission
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from ..serializers import BookWriteSerializer,  BookListSerializer



class BookCreateAPIView(CreateAPIView):
    serializer_class = BookWriteSerializer

    def get_permissions(self):
        self.allowed_roles = ["ADMIN", "LIBRARIAN"]
        return [RolePermission()]
    
    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()


class BookListAPIView(ListAPIView):
    serializer_class = BookListSerializer

    def get_permissions(self):
        return [IsAuthenticated()]
    
    def get_queryset(self):
        return Book.objects.select_related("publisher").prefetch_related("authors", "categories")


class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    lookup_field = "id"

    def get_queryset(self):
        return Book.objects.select_related("publisher").prefetch_related("authors", "categories")
    
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.allowed_roles = ["ADMIN", "LIBRARIAN"]
            return [RolePermission()]
        
        elif self.request.method == "DELETE":
            self.allowed_roles = "ADMIN"
            return [RolePermission()]
        
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.serializer_class = BookWriteSerializer
        self.serializer_class = BookListSerializer
