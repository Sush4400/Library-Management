from rest_framework.views import APIView, Response


# Create your views here.
class BorrowBookView(APIView):
    def post(self, request):
        pass


class ReturnBookView(APIView):
    def post(self, request):
        pass


class BorrowHistoryView(APIView):
    def get(self, request):
        pass


class UserBorrowedBooksView(APIView):
    def get(self, request, user_id):
        pass
