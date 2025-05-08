from django.contrib import admin
from django.contrib.auth.models import Permission, Group
from apps.identity.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'role', 'is_active', 'is_staff', 'deleted_at')
    list_filter = ('is_active',)
    search_fields = ('email',)
    readonly_fields = ('deleted_at',)
    actions = ['restore_users']

    # Add horizontal filters for permissions and groups
    filter_horizontal = ('user_permissions', 'groups')

    @admin.action(description='Restore selected users')
    def restore_users(self, request, queryset):
        """
        This function restores the selected users by setting them as active
        and clearing the deleted_at timestamp.
        """
        updated = queryset.filter(is_active=False, deleted_at__isnull=False).update(is_active=True, deleted_at=None)

        if updated:
            self.message_user(request, f"{updated} user(s) restored successfully.")
        else:
            self.message_user(request, "No inactive users found or users already restored.", level='warning')

    def get_user_permissions(self, obj):
        """
        Displays the permissions associated with a user in the admin.
        """
        return ", ".join([perm.name for perm in obj.user_permissions.all()])
    
    get_user_permissions.short_description = 'User Permissions'

    def save_model(self, request, obj, form, change):
        """
        Save the user model, considering the modification of permissions and groups.
        """
        super().save_model(request, obj, form, change)

        if 'user_permissions' in form.changed_data:
            obj.user_permissions.set(form.cleaned_data['user_permissions'])

        if 'groups' in form.changed_data:
            obj.groups.set(form.cleaned_data['groups'])

        if obj.role == 'Administrator':
            obj.user_permissions.set(Permission.objects.all())

admin.site.register(User, UserAdmin)
admin.site.register(Permission)
