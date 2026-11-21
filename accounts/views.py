from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from .serailizers import *


class RegisterView(APIView):
    serializer_class = RegisterSerailizer
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerailizer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({"message": "Registration successful","user": serializer.data}, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerailizer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = authenticate(username=username,password=password)
        if user is None:

            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response({"message": "Login successful","user": UserSerailizer(user).data,"refresh": str(refresh),"access": str(refresh.access_token)}, status=status.HTTP_200_OK)



class RefreshView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshSerailizer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data.get("refresh")
        try:
            token = RefreshToken(refresh)
            return Response({"access": str(token.access_token)}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        
class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerailizer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data.get("refresh")

        try:
            token = RefreshToken(refresh)
            if str(token["user_id"]) != str(request.user.id):

                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerailizer(request.user)
        return Response(serializer.data)


    def put(self, request):
        serializer = UserSerailizer(request.user,data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)