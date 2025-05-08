from apps.identity.services.auth_service import AuthService
from apps.identity.serializers import UserDetailSerializer as UserSerializer


class LoginUserUseCase:
    """
    Handles the login process using AuthService and returns user info + tokens.
    """
    def execute(self, email: str, password: str):
        user = AuthService.authenticate_user(email=email, password=password)
        tokens = AuthService.generate_tokens(user)
        user_data = UserSerializer(user).data
        return {
            "tokens": tokens,
            "user": user_data
        }
