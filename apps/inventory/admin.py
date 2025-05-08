from django.contrib import admin
from .models import InventoryItem

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'purchase_price', 'sale_price', 'currency', 'is_active', 'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'deleted_by', 'transaction_type', 'alert', 'profit')
    list_filter = ('is_active', 'product', 'transaction_type', 'alert', 'created_by', 'updated_by')
    search_fields = ('product__name', 'created_by__email', 'updated_by__email')
    readonly_fields = ('created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'deleted_by')

    def profit(self, obj):
        return obj.profit
    profit.short_description = 'Profit'

    def get_price(self, obj):
        if obj.transaction_type == 'purchase':
            return obj.purchase_price
        elif obj.transaction_type == 'sale':
            return obj.sale_price
        return "N/A"

    get_price.short_description = 'Price'


    def alert(self, obj):
        return "Alert" if obj.alert else "Normal"
    alert.short_description = "Stock Alert"

admin.site.register(InventoryItem, InventoryItemAdmin)
