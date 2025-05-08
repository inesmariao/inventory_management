from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed


class AuthService:
    """
    Authenticates a user and issues JWT tokens.
    """
    @staticmethod
    def authenticate_user(email: str, password: str):
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid email or password")
        return user

    @staticmethod
    def generate_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
