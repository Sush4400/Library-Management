from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from ..models import *
from django.db import transaction
from core.pemissions import RolePermission


# Create your views here.
# AUTHOR
class AuthorCreateView(APIView):
    permission_classes = [RolePermission]
    allowed_roles = ["ADMIN", "LIBRARIAN"]

    def post(self, request):
        try:
            data = request.data
            name = data.get("name")
            dob = data.get("dob")
            nationality = data.get("nationality")

            if not name:
                return Response({"status": False, "message": "Name is Required!!"}, status=400)
            
            with transaction.atomic():
                author = Author.objects.create(
                    name=name, dob=dob, nationality=nationality
                )

            return Response({
                "status": True,
                "message": "Author created successfully.",
                "author_id": author.id
            }, status=201)
        
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)


class AuthorListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            authors = Author.objects.filter(is_deleted=False).only(
                "id", "name", "dob", "nationality", "is_active"
            )
            results = [
                {
                    "author_id": author.id,
                    "name": author.name,
                    "dob": author.dob.isoformat() if author.dob else None,
                    "nationality": author.nationality,
                    "is_active": author.is_active
                }
                for author in authors
            ]
            return Response({"status": True, "results": results}, status=200)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)


class AuthorDetailView(APIView):
    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id, is_deleted=False)

            return Response({
                "status": True,
                "results": {
                    "author_id": author.id,
                    "name": author.name,
                    "dob": author.dob.isoformat() if author.dob else None,
                    "nationality": author.nationality,
                    "is_active": author.is_active
                }
            }, status=200)
        
        except Author.DoesNotExist:
            return Response({"status": False, "message": "Invalid Author ID."}, status=404)
        
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)


class AuthorUpdateView(APIView):
    permission_classes = [RolePermission]
    allowed_roles = ["ADMIN", "LIBRARIAN"]
    
    def put(self, request, author_id):
        try:
            data = request.data
            author = Author.objects.get(id=author_id, is_deleted=False)
            name = data.get("name")
            dob = data.get("dob")
            nationality = data.get("nationality")

            if name is not None:
                author.name = name

            if dob is not None:
                author.dob = dob

            if nationality is not None:
                author.nationality = nationality

            author.save()
            
            return Response({"status": True, "message": "Author updated successfully."}, status=200)

        except Author.DoesNotExist:
            return Response({"status": False, "message": "Invalid Author ID."}, status=404)

        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)
    

class AuthorDeleteView(APIView):
    permission_classes = [RolePermission]
    allowed_roles = ["ADMIN"]

    def delete(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id, is_deleted=False)

            author.is_deleted = True
            author.save(update_fields=["is_deleted"])
            return Response({"status": True, "message": "Author deleted successfully."}, status=200)

        except Author.DoesNotExist:
            return Response({"status": False, "message": "Invalid Author ID."}, status=404)

        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)