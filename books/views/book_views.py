from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models import *
from django.db import transaction
from core.pemissions import RolePermission



class BookCreateView(APIView):
    def post(self, request):
        pass


class BooksListView(APIView):
    def get(self, request):
        return Response({"status": True, "message": "Books Fetched."})



class BookDetailView(APIView):
    def get(self, request, book_id):
        pass


class BookUpdateView(APIView):
    def post(self, request):
        pass


class BookDeleteView(APIView):
    def post(self, request):
        pass
