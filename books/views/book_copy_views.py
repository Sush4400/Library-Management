from rest_framework.permissions import IsAuthenticated
from ..models import *
from django.db import transaction
from core.permissions import RolePermission
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..serializers import BookCopySerializer


class BookListCreateView(ListCreateAPIView):
    serializer_class = BookCopySerializer

    def get_queryset(self):
        return BookCopy.objects.select_related('book').filter(is_deleted=False).only(
            'shelf_location', 'status', 'barcode'
        )
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.allowed_roles = ["ADMIN", "LIBRARIAN"]
            return [RolePermission()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()


class BookCopyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookCopySerializer
    lookup_field = "id"

    def get_queryset(self):
        return BookCopy.objects.select_related("book").filter(is_deleted=False)
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            self.allowed_roles = ["ADMIN", "LIBRARIAN"]
            return [RolePermission()]
        
        if self.request.method == 'DELETE':
            self.allowed_roles = ["ADMIN"]
            return [RolePermission()]
        
        return [IsAuthenticated()]
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])
