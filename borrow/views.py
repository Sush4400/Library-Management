from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from .services.borrow_service import BorrowService
from .services.return_service import ReturnService
from .serializers import BorrowSerializer
from core.permissions import RolePermission
from .models import Borrow
from users.models import User


# Create your views here.
class BorrowBookView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        book_id = request.data.get("book_id")

        borrow = BorrowService.borrow_book(
            user=request.user,
            book_id=book_id
        )
        
        serialzer = BorrowSerializer(borrow)
        return Response({"status": True, "data": serialzer.data})


class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        borrow_id = request.data.get("borrow_id")
        borrow = ReturnService.return_book(borrow_id=borrow_id)
        serializer = BorrowSerializer(borrow)
        return Response({"status": True, "data": serializer.data})


class BorrowHistoryView(APIView):
    permission_classes = [RolePermission]
    allowed_roles = ["ADMIN", "LIBRARIAN"]
    def get(self, request):
        borrows = Borrow.objects.select_related(
            "user", "book_copy", "book_copy__book"
        ).all().order_by("-borrow_date")

        data = []
        for borrow in borrows:
            data.append({
                "borrow_id": borrow.id,
                "user_id": borrow.user.id,
                "username": borrow.user.username,
                "book_title": borrow.book_copy.book.title,
                "copy_id": borrow.book_copy.id,
                "borrow_date": borrow.borrow_date,
                "due_date": borrow.due_date,
                "return_date": borrow.return_date,
                "fine": borrow.fine_amount,
                "is_returned": borrow.is_returned
            })

        return Response({"status": True, "results": data})


class UserBorrowedBooksView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            borrows = Borrow.objects.select_related(
                "book_copy", "book_copy__book"
            ).filter(user=user).order_by("-borrow_date")

            data = []
            for borrow in borrows:
                data.append({
                    "borrow_id": borrow.id,
                    "book_title": borrow.book_copy.book.title,
                    "copy_id": borrow.book_copy.id,
                    "borrow_date": borrow.borrow_date,
                    "due_date": borrow.due_date,
                    "return_date": borrow.return_date,
                    "fine": borrow.fine_amount,
                    "is_returned": borrow.is_returned
                })

            return Response(({"status": True, "results": data}), status=200)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)