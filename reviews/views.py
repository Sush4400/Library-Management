from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Review
from core.permissions import RolePermission
from rest_framework.permissions import IsAuthenticated
from .serializers import ReviewSerializer


# Create your views here.
class ReviewAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def get_permissions(self):
        if self.request.method == "POST":
            self.allowed_roles = ["ADMIN", "LIBRARIAN"]
            return [RolePermission()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save()
    

class ReviewRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    lookup_field = "id"

    def get_queryset(self):
        return Review.objects.all()

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            self.allowed_roles = ["ADMIN", "LIBRARIAN"]
            return [RolePermission()]
        elif self.request.method == "DELETE":
            self.allowed_roles = ["ADMIN"]
            return [RolePermission()]
        return [IsAuthenticated()]

    # def perform_destroy(self, instance):
    #     instance.is_deleted = True
    #     instance.save(update_fields=["is_deleted"])