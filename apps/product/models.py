from django.db import models

class Product(models.Model):
    """
    Model representing a product with its details.
    """
    CURRENCY_CHOICES = (
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('COP', 'Colombian Peso'),
        ('MXN', 'Mexican Peso'),
        ('GBP', 'British Pound'),
        ('JPY', 'Japanese Yen'),
        ('AUD', 'Australian Dollar'),
    )

    company = models.ForeignKey('company.Company', related_name='products', on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    characteristics = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES, default='COP')
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this product should be treated as active."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the product was created."
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the product was deactivated (soft deleted)."
    )

    def __str__(self):
        return f"{self.name} ({self.code})"
