from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'nit', 'country', 'department', 'municipality',
        'is_active', 'deleted_at', 'created_at'
    )
    list_filter = ('is_active', 'country')
    search_fields = ('name', 'nit')
    readonly_fields = ('deleted_at', 'created_at')
