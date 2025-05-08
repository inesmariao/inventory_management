from apps.identity.models import User
from django.shortcuts import get_object_or_404


class UserService:
    @staticmethod
    def list_users():
        return User.objects.all()

    @staticmethod
    def retrieve_user(user_id):
        return get_object_or_404(User, pk=user_id)

    @staticmethod
    def delete_user(user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return user
