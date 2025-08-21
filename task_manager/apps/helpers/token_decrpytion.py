import jwt
from rest_framework import serializers
from django.conf import settings
from apps.users_management.models import UserManagement

class JWTUserMixin:
    """
    Mixin to fetch the logged-in user from JWT in Authorization header.
    """

    def get_user_from_jwt(self):
        request = self.context.get("request")
        if not request:
            raise serializers.ValidationError("Request context is missing.")

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise serializers.ValidationError("Authorization header missing or invalid.")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            username = payload.get("username")
            if not username:
                raise serializers.ValidationError("Username not found in token.")

            user = UserManagement.objects.get(username=username)
            return user

        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError("Token has expired.")
        except jwt.InvalidTokenError:
            raise serializers.ValidationError("Invalid token.")
        except UserManagement.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
