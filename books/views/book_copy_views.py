from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import *
from django.db import transaction
from core.pemissions import RolePermission



class BookCopyCreateView(APIView):
    def post(self, request):
        pass


class BookCopyListView(APIView):
    def get(self, request):
        pass


class BookCopyUpdateView(APIView):
    def put(self, request, copy_id):
        pass


class BookCopyDeleteView(APIView):
    def delete(self, request, copy_id):
        pass
