from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from ..models import *
from django.db import transaction
from core.permissions import RolePermission
from rest_framework import generics
from ..serializers import CategorySerializer


# name, description, is_active
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):

        if self.request.method == "POST":
            self.allowed_roles = ["ADMIN", "LIBRARIAN"]
            return [RolePermission()]

        return [IsAuthenticated()]


class CategoryRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    print("here")
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "id"
    
    def get_permissions(self):

        if self.request.method in ["PUT", "PATCH"]:
            self.allowed_roles = ["ADMIN", "LIBRARIAN"]
            return [RolePermission()]

        if self.request.method == "DELETE":
            self.allowed_roles = ["ADMIN"]
            return [RolePermission()]

        return [IsAuthenticated()]
