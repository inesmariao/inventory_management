from rest_framework import serializers
from .models import InventoryItem

class InventoryItemSerializer(serializers.ModelSerializer):
    product_price = serializers.ReadOnlyField(source='product.price')
    profit = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'product', 'quantity', 'purchase_price', 'sale_price', 'currency', 'is_active', 'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'deleted_by', 'transaction_type', 'alert', 'profit']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'deleted_by', 'profit']

    def validate(self, attrs):
        transaction_type = attrs.get('transaction_type')
        if transaction_type == 'purchase' and not attrs.get('purchase_price'):
            raise serializers.ValidationError("Purchase price is required for purchase transactions.")
        if transaction_type == 'sale' and not attrs.get('sale_price'):
            raise serializers.ValidationError("Sale price is required for sale transactions.")

        if transaction_type not in ['purchase', 'sale']:
            raise serializers.ValidationError("Transaction type must be either 'purchase' or 'sale'.")

        return attrs

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['created_by'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        validated_data['updated_by'] = user
        return super().update(instance, validated_data)
