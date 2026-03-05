from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from ..models import *
from django.db import transaction
from core.pemissions import RolePermission



class PublisherCreateView(APIView):
    permission_classes = [RolePermission]
    allowed_roles = ["ADMIN", "LIBRARIAN"]

    def post(self, request):
        try:
            data = request.data
            name = data.get("name")
            email = data.get("email")

            if not name:
                return Response({"status": False, "message": "Name is Required!!"}, status=400)
            
            if not email:
                return Response({"status": False, "message": "Email is Required!!"}, status=400)
            
            with transaction.atomic():
                publisher = Publisher.objects.create(
                    name=name,
                    address=data.get("address"),
                    website=data.get("website"),
                    email=email,
                    phone=data.get("phone"),
                )
            
            return Response({
                "status": True,
                "message": "Publisher Created Successfully",
                "publisher_id": publisher.id
            }, status=201)
        
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)


class PublisherListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            publishers = Publisher.objects.filter(is_deleted=False).only(
                'name', 'address', 'website', 'email', 'phone'
            )
            results = [
                {
                    "name": publisher.name,
                    "address": publisher.address,
                    "website": publisher.website,
                    "email": publisher.email,
                    "phone": publisher.phone
                }
                for publisher in publishers
            ]
            return Response({"status": True, "results": results}, status=200)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)


class PublisherDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, publisher_id):
        try:
            publisher = Publisher.objects.get(id=publisher_id, is_deleted=False)

            return Response({
                "name": publisher.name,
                "address": publisher.address,
                "website": publisher.website,
                "email": publisher.email,
                "phone": publisher.phone
            }, status=200)

        except Publisher.DoesNotExist:
            return Response({"stautus": False, "message": "Invalid Publisher ID!"}, status=404)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)


class PublisherUpdateView(APIView):
    permission_classes = [RolePermission]
    allowed_roles = ["ADMIN", "LIBRARIAN"]

    def put(self, request, publisher_id):
        try:
            data = request.data
            name = data.get("name")
            email = data.get("email")
            address = data.get("address")
            website = data.get("website")
            phone = data.get("phone")

            publisher = Publisher.objects.get(id=publisher_id, is_deleted=False)

            if name:
                publisher.name = name

            if email:
                publisher.email = email

            if phone:
                publisher.phone = phone

            if website:
                publisher.website = website

            if address:
                publisher.address = address

            publisher.save()

            return Response({"status": True, "message": "Publisher Updated Successfully."}, status=200)

        except Publisher.DoesNotExist:
            return Response({"status": False, "message": "Invalid Publisher ID"}, status=404)

        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)


class PublisherDeleteView(APIView):
    permission_classes = [RolePermission]
    allowed_roles = ["ADMIN"]
    
    def delete(self, request, publisher_id):
        try:
            publisher = Publisher.objects.get(id=publisher_id, is_deleted=False)
            publisher.is_deleted = True
            publisher.save(update_fields=["is_deleted"])
            return Response({"status": True, "message": "Publisher Deleted Successfully."}, status=200)
        
        except Publisher.DoesNotExist:
            return Response({"status": False, "message": "Invalid Publisher ID"}, status=404)
        
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)
