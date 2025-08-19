from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import LoginSerializer
from rest_framework.permissions import AllowAny

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            response = Response({
                "message": "Login successful",
                "user": data
            }, status=status.HTTP_200_OK)

            # set JWT in cookies
            response.set_cookie(
                key="access_token",
                value=data["access"],
                httponly=True,
                secure=True,  # change to True in production with HTTPS
                samesite="Lax"
            )
            response.set_cookie(
                key="refresh_token",
                value=data["refresh"],
                httponly=True,
                secure=True,
                samesite="Lax"
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
