from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Product
from .serializers import ProductSerializer
from apps.identity.role_permissions import IsAdmin
from drf_spectacular.utils import extend_schema, OpenApiResponse

class ProductCreateView(generics.CreateAPIView):
    """
    Allows an admin to create a new product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class ProductListView(generics.ListAPIView):
    """
    Returns a list of all active products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

class ProductDetailView(generics.RetrieveAPIView):
    """
    Returns detailed information of a specific product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

class ProductUpdateView(generics.UpdateAPIView):
    """
    Allows an admin to update an existing product's information.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'pk'

@extend_schema(
    description="Soft deletes a product by marking it as inactive.",
    responses={
        200: OpenApiResponse(description="Product deactivated."),
        404: OpenApiResponse(description="Product not found.")
    }
)
class ProductSoftDeleteView(APIView):
    """
    Soft deletes a product by marking the product as inactive and storing the deleted_at timestamp.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            product.is_active = False
            product.deleted_at = timezone.now()
            product.save()
            return Response({'message': 'Product deactivated successfully.'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    description="Restores a previously deactivated (soft deleted) product.",
    responses={
        200: OpenApiResponse(description="Product restored."),
        400: OpenApiResponse(description="Product is already active."),
        404: OpenApiResponse(description="Product not found.")
    }
)
class ProductRestoreView(APIView):
    """
    Restores a previously deactivated (soft deleted) product.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            if product.is_active:
                return Response({'message': 'Product is already active.'}, status=status.HTTP_400_BAD_REQUEST)
            product.is_active = True
            product.deleted_at = None
            product.save()
            return Response({'message': 'Product restored successfully.'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
