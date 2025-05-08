from apps.identity.services.user_service import UserService


class ManageUsersUseCase:
    def list(self):
        return UserService.list_users()

    def retrieve(self, user_id):
        return UserService.retrieve_user(user_id)

    def delete(self, user_id):
        return UserService.delete_user(user_id)
