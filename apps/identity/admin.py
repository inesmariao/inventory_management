from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'role', 'is_active', 'is_staff', 'deleted_at')
    list_filter = ('is_active',)
    search_fields = ('email',)
    readonly_fields = ('deleted_at',)
    actions = ['restore_users']

    @admin.action(description='Restore selected users')
    def restore_users(self, request, queryset):
        updated = queryset.update(is_active=True, deleted_at=None)
        self.message_user(request, f"{updated} user(s) restored successfully.")
