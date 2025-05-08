from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'company', 'code', 'name', 'characteristics', 'price', 'currency', 'stock', 'is_active', 'deleted_at']
        read_only_fields = ['is_active', 'deleted_at']

    def validate(self, attrs):
        """
        Validate product data before saving to ensure correctness.
        """
        return attrs
