from rest_framework.views import APIView, Response
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .tasks import send_welcome_email


'''
always hash the password:
from django.contrib.auth.hashers import make_password
password = make_password(password)

or by create_user:
user = User.objects.create_user(...)
'''


# Create your views here.
class UsersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            users = User.objects.filter(is_superuser=False, is_staff=False)
            results = [
                {
                    "user_id": user.id,
                    "full_name": user.full_name,
                    "phone_number": user.phone_number,
                    "email": user.email,
                    "role": user.role,
                    "is_active": user.is_active
                }
                for user in users
            ]
            
            return Response({"status": True, "results": results}, status=200)
        
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)
        
    def post(self, request):
        data = request.data
        try:
            username = data.get("username")
            email = data.get("email")
            phone_number = data.get("phone_number")
            full_name = data.get("full_name")

            existing_user = User.objects.filter(
                Q(username=username) | Q(email=email) | Q(phone_number=phone_number)
            ).first()

            if existing_user:
                if existing_user.username == username:
                    message = "Username Already Exists!"
                if existing_user.email == email:
                    message = "Email Already Exists!"
                if existing_user.phone_number == phone_number:
                    message = "Phone Number Already Exists!"
                return Response({"status": False, "message": message}, status=400)

            user = User.objects.create_user(
                username=data.get("username"),
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                password=data.get("password")
            )

            send_welcome_email.delay(user.email, user.full_name)

            return Response({
                "status": True,
                "message": "User Created Successfully.",
                "user_id": user.id
            }, status=201)
        
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=500)    
        

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        print(f"username: {username}, password: {password}")

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"status": False, "message": "Invalid Credential!!"})
        
        refresh_token = RefreshToken.for_user(user)

        return Response({
            "status": True,
            "refresh_token": str(refresh_token),
            "access_token": str(refresh_token.access_token),
            "role": user.role
        })
    

# only refresh token can be blacklisted.
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({
                "status": False,
                "message": "Refresh token required"
            }, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "status": True,
                "message": "Logout successful"
            })

        except Exception:
            return Response({
                "status": False,
                "message": "Invalid token"
            }, status=400)