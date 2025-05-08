from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.utils import timezone
from apps.identity.serializers import LoginSerializer, UserCreateSerializer, UserDetailSerializer
from apps.identity.use_cases.login_user import LoginUserUseCase
from apps.identity.role_permissions import IsAdmin
from apps.identity.models import User


@extend_schema(request=LoginSerializer, responses={200: None})
class LoginView(APIView):
    """
    Handles the login process by validating credentials and generating JWT tokens.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = LoginUserUseCase()
        result = use_case.execute(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        return Response(result, status=status.HTTP_200_OK)

class UserCreateView(generics.CreateAPIView):
    """
    Allows an admin to create a new user in the system.
    """
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]


class UserListView(generics.ListAPIView):
    """
    Returns a list of all active users.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class UserDetailView(generics.RetrieveAPIView):
    """
    Returns detailed information of a user.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'pk'


class UserUpdateView(generics.UpdateAPIView):
    """
    Allows an admin to update an existing user's information.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'pk'


class UserSoftDeleteView(APIView):
    """
    Soft deletes a user by setting is_active=False and storing deleted_at timestamp.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = False
            user.deleted_at = timezone.now()
            user.save()
            return Response({'message': 'User deactivated successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    description="Restores a previously deactivated (soft deleted) user.",
    responses={
        200: OpenApiResponse(description="User restored successfully."),
        400: OpenApiResponse(description="User is already active."),
        404: OpenApiResponse(description="User not found.")
    }
)
class UserRestoreView(APIView):
    """
    Allows an admin to restore a soft-deleted user.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            if user.is_active:
                return Response({'message': 'User is already active.'}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.deleted_at = None
            user.save()
            return Response({'message': 'User restored successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
