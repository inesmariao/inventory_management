from django.db import models
from apps.product.models import Product
from django.conf import settings
from django.utils import timezone

class InventoryItem(models.Model):
    """
    Model to manage product inventory.
    Tracks quantity, price, and the state of each product in the inventory.
    """
    TRANSACTION_TYPE_CHOICES = (
        ('purchase', 'Purchase'),
        ('sale', 'Sale')
    )

    product = models.ForeignKey(Product, related_name='inventory_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Quantity of the product in stock.")
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Purchase price of the product."
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Sale price of the product."
    )
    currency = models.CharField(max_length=10, choices=Product.CURRENCY_CHOICES, default='COP')
    is_active = models.BooleanField(
      default=True,
      help_text="Indicates whether this inventory item is active."
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
        default='purchase',
        help_text="Type of transaction: 'purchase' for adding stock, 'sale' for reducing stock."
    )
    profit = models.DecimalField(
      max_digits=10,
      decimal_places=2,
      default=0.0,
      help_text="Profit from the transaction"
    )
    alert = models.BooleanField(
        default=False,
        help_text="Indicates if stock is below the alert threshold (5 units)."
    )
    created_at = models.DateTimeField(
      auto_now_add=True,
      help_text="Timestamp when the inventory item was created."
    )
    updated_at = models.DateTimeField(
      auto_now=True,
      help_text="Timestamp when the inventory item was last updated."
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      related_name='created_inventory_items',
      null=True,
      on_delete=models.SET_NULL
    )
    updated_by = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      related_name='updated_inventory_items',
      null=True,
      on_delete=models.SET_NULL
    )
    deleted_by = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      related_name='deleted_inventory_items',
      null=True,
      blank=True,
      on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"Inventory Item {self.product.name} - {self.quantity} units"

    class Meta:
        verbose_name = "Inventory Item"
        verbose_name_plural = "Inventory Items"