from rest_framework.views import APIView, Response


# Create your views here.
class Books(APIView):
    def get(self, request):
        return Response({"status": True, "message": "Books Fetched."})