from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from ..models import *
from django.db import transaction
from core.pemissions import RolePermission


# name, description, is_active
class CategoryCreateView(APIView):
    permission_classes = [RolePermission]
    allowed_roles = ["ADMIN", "LIBRARIAN"]

    def post(self, request):
        try:
            data = request.data
            name = data.get("name")

            if not name:
                return Response({"status": False, "message": "Name is Required"}, status=400)
            
            with transaction.atomic:
                category = Category.objects.create(
                    name=name,
                    description=data.get("description"),
                )

            return Response({
                "status": True,
                "message": "Category Created.",
                "cateogory_id": category.id
            }, status=201)
        
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)


class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            categories = Category.objects.filter(is_deleted=False).only(
                "name", "description", "is_active"
            )
            results = [
                {
                    "name": category.name,
                    "description": category.description,
                    "is_active": category.is_active
                }
                for category in categories
            ]

            return Response({"status": True, "results": results}, status=200)

        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)


class CategoryUpdateView(APIView):
    permission_classes = [RolePermission]
    allowed_roles = ["ADMIN", "LIBRARIAN"]

    def put(self, request, category_id):
        try:
            data = request.data
            name = data.get("name")
            description = data.get("description")
            is_active = data.get("is_active")

            category = Category.objects.get(id=category_id)
            if name: category.name = name
            if description: category.description = description
            if is_active: category.is_active = is_active
            category.save()

            return Response({"status": True, "message": "Category Updated."}, status=200)

        except Category.DoesNotExist:
            return Response({"status": False, "message": "Invalid Category ID!!"}, status=500)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)


class CategoryDeleteView(APIView):
    permission_classes = [RolePermission]
    allowed_roles = ["ADMIN"]

    def delete(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id)
            category.is_deleted = True
            category.save(update_fields=["is_deleted"])
            return Response({"status": True, "message": "Category Deleted."}, status=200)

        except Category.DoesNotExist:
            return Response({"status": False, "message": "Invalid Category ID!!"}, status=500)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)
