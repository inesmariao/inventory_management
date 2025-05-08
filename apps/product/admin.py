from django.contrib import admin
from .models import Product
from django.utils import timezone


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'company', 'price', 'currency', 'stock', 'is_active', 'deleted_at')
    list_filter = ('company', 'currency', 'is_active')
    search_fields = ('name', 'code', 'company__name')
    readonly_fields = ('deleted_at',)
    ordering = ('-created_at',)

    actions = ['soft_delete_products', 'restore_products']

    def soft_delete_products(self, request, queryset):
        """
        Soft delete selected products by setting is_active to False.
        """
        queryset.update(is_active=False, deleted_at=timezone.now())
        self.message_user(request, f"{queryset.count()} products deactivated.")

    def restore_products(self, request, queryset):
        """
        Restore selected products by setting is_active to True.
        """
        queryset.update(is_active=True, deleted_at=None)
        self.message_user(request, f"{queryset.count()} products restored.")
