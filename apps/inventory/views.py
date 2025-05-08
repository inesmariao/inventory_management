from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework import generics
from .models import InventoryItem
from .serializers import InventoryItemSerializer
from rest_framework.permissions import IsAuthenticated
from apps.identity.role_permissions import IsAdmin

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'product', 'quantity', 'purchase_price', 'sale_price','currency', 'is_active', 'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'deleted_by']
        read_only_fields = ['created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'deleted_by']

    def validate(self, attrs):
        return attrs


class InventoryItemCreateView(generics.CreateAPIView):
    """
    Allows an admin to create a new inventory item and associate it with the user performing the action.
    """
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        """
        Create the inventory item and update the stock based on the transaction type.
        """
        transaction_type = self.request.data.get('transaction_type')
        if not transaction_type:
            raise serializers.ValidationError("Transaction type is required.")

        purchase_price = self.request.data.get('purchase_price')
        sale_price = self.request.data.get('sale_price')

        if transaction_type == 'purchase' and not purchase_price:
            raise serializers.ValidationError("Purchase price is required for purchase transactions.")
        if transaction_type == 'sale' and not sale_price:
            raise serializers.ValidationError("Sale price is required for sale transactions.")

        serializer.save(created_by=self.request.user)

        product = serializer.instance.product
        quantity = serializer.validated_data['quantity']
        profit = 0.0

        if transaction_type == 'purchase':
            product.stock += quantity
            profit = 0.0
        elif transaction_type == 'sale':
            if product.stock < quantity:
                raise serializers.ValidationError("Not enough stock for the sale.")
            product.stock -= quantity
            profit = (float(sale_price) - float(purchase_price)) * quantity
        else:
            raise serializers.ValidationError("Invalid transaction type")

        product.save()

        serializer.instance.profit = profit
        serializer.instance.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InventoryItemListView(generics.ListAPIView):
    """
    Returns a list of all active inventory items.
    """
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(is_active=True)

class InventoryItemDetailView(generics.RetrieveAPIView):
    """
    Returns detailed information of a specific inventory item.
    """
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class InventoryItemUpdateView(generics.UpdateAPIView):
    """
    Allows an admin to update an existing inventory item's details and associate the user who updated it.
    """
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class InventoryItemDeleteView(APIView):
    """
    Soft deletes an inventory item by setting is_active=False and storing the deleted_at timestamp.
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = InventoryItemSerializer

    def delete(self, request, pk):
        try:
            inventory_item = InventoryItem.objects.get(pk=pk)

            inventory_item.is_active = False
            inventory_item.deleted_at = timezone.now()
            inventory_item.deleted_by = request.user
            inventory_item.save()

            return Response({"message": "Inventory item deactivated successfully."}, status=status.HTTP_200_OK)

        except InventoryItem.DoesNotExist:
            return Response({"error": "Inventory item not found."}, status=status.HTTP_404_NOT_FOUND)
