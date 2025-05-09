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
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import InventoryItem
from django.core.mail import EmailMessage
from decouple import config

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

def generate_inventory_pdf(request):
    inventory_items = InventoryItem.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)

    # PDF title
    p.drawString(200, 750, "Inventory Report")

    y_position = 730

    # Columns for the report
    p.drawString(40, y_position, "Product")
    p.drawString(200, y_position, "Quantity")
    p.drawString(300, y_position, "Purchase Price")
    p.drawString(400, y_position, "Sale Price")
    p.drawString(500, y_position, "Profit")

    y_position -= 20

    # Print the inventory items on the PDF
    for item in inventory_items:
        p.drawString(40, y_position, str(item.product.name))
        p.drawString(200, y_position, str(item.quantity))
        p.drawString(300, y_position, str(item.purchase_price))
        p.drawString(400, y_position, str(item.sale_price))
        p.drawString(500, y_position, str(item.profit))
        y_position -= 20

        if y_position < 100:
            p.showPage()
            p.setFont("Helvetica", 12)
            y_position = 750
            p.drawString(40, y_position, "Product")
            p.drawString(200, y_position, "Quantity")
            p.drawString(300, y_position, "Purchase Price")
            p.drawString(400, y_position, "Sale Price")
            p.drawString(500, y_position, "Profit")
            y_position -= 20

    p.showPage()
    p.save()

    return response


def send_inventory_pdf_email(request):
    response = generate_inventory_pdf(request)
    pdf_content = response.content

    email_subject = "Inventory Report"
    email_body = """
    Dear recipient,

    Please find attached the inventory report PDF for your reference.

    If you have any questions, feel free to reach out.

    Best regards,
    LiteThinking
    """

    recipient_email = config('EMAIL_RECIPIENT')

    from_email = config('DEFAULT_FROM_EMAIL')

    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=from_email,
        to=[recipient_email]
    )

    email.attach('inventory_report.pdf', pdf_content, 'application/pdf')

    try:
        email.send()
        return HttpResponse("Email sent successfully.")
    except Exception as e:
        return HttpResponse(f"Failed to send email. Error: {str(e)}")



