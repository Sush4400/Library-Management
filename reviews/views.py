from rest_framework.views import APIView, Response


# Create your views here.
class Reviews(APIView):
    def get(self, request):
        return Response({"status": True, "message": "Reviews Fetched."})