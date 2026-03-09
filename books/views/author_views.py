from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from ..models import Author
from ..serializers import AuthorSerializer
from core.permissions import RolePermission


class AuthorListCreateView(ListCreateAPIView):

    serializer_class = AuthorSerializer

    def get_queryset(self):
        return Author.objects.filter(is_deleted=False).only(
            "id", "name", "dob", "nationality", "is_active"
        )

    def get_permissions(self):

        if self.request.method == "POST":
            self.allowed_roles = ["ADMIN", "LIBRARIAN"]
            return [RolePermission()]

        return [IsAuthenticated()]

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()


class AuthorDetailView(RetrieveUpdateDestroyAPIView):

    serializer_class = AuthorSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Author.objects.filter(is_deleted=False)

    def get_permissions(self):

        if self.request.method in ["PUT", "PATCH"]:
            self.allowed_roles = ["ADMIN", "LIBRARIAN"]
            return [RolePermission()]

        if self.request.method == "DELETE":
            self.allowed_roles = ["ADMIN"]
            return [RolePermission()]

        return [IsAuthenticated()]

    def perform_destroy(self, instance):
        # soft delete
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])