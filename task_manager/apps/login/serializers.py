from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from apps.users_management.models import UserManagement
from rest_framework import status

# Import the custom token serializer we just created.
# You might need to adjust the import path based on your project structure.
# from .serializers import MyTokenObtainPairSerializer # Assuming it's in the same app's serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # We'll create it here for clarity

# ===================================================================
# STEP 1: Define the Custom Token Serializer with Custom Claims
# ===================================================================
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes the JWT token creation process to include additional
    user details in the token's payload.
    """
    @classmethod
    def get_token(cls, user):
        """
        Overrides the default token generation to add custom user data.
        """
        # Get the base token with default claims
        token = super().get_token(user)

        # Add custom claims (user details) to the token payload
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token

# ===================================================================
# STEP 2: Refactor the LoginSerializer
# ===================================================================
class LoginSerializer(serializers.Serializer):
    """
    This serializer handles user authentication.
    It takes 'username' and 'password', validates them, and returns
    access and refresh tokens with user details embedded in the access token's payload.
    """
    # Define the fields required for login.
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        This method validates the user's credentials and generates the tokens.
        """
        # Retrieve username and password from the input data.
        username = data.get("username")
        password = data.get("password")

        # Attempt to retrieve an active, non-deleted user from the database.
        try:
            user = UserManagement.objects.get(username=username, is_active=True, is_deleted=False)
        except UserManagement.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")

        # Use Django's secure check_password function to validate the password.
        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid username or password")

        # ==================== TOKEN GENERATION LOGIC ====================
        # Instantiate our custom token serializer with the user object.
        token_serializer = MyTokenObtainPairSerializer.get_token(user)

        # The token_serializer object now contains our custom claims.
        # We can get the access and refresh tokens from it.
        refresh = str(token_serializer)
        access = str(token_serializer.access_token)
        # =================================================================

        # Prepare the data for the API response.
        # The user details are now encoded within the 'access' token.
        # We no longer need to return a separate 'user' object.
        response_data = {
            "Status":"User LoggedIn Successfully",
            "Status Code":status.HTTP_200_OK,
            "refresh": refresh,
            "access": access,
        }

        return response_data