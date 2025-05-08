from django.db import models
from django.utils import timezone


class Country(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the country")
    alpha_2 = models.CharField(max_length=2, unique=True)
    alpha_3 = models.CharField(max_length=3, unique=True)
    numeric_code = models.IntegerField()

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the department")
    country = models.ForeignKey(Country, related_name='departments', on_delete=models.CASCADE)
    code = models.IntegerField()

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the municipality")
    department = models.ForeignKey(Department, related_name='municipalities', on_delete=models.CASCADE)
    code = models.IntegerField()

    def __str__(self):
        return self.name


class Company(models.Model):
    nit = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='companies')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='companies')
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, null=True, related_name='companies')

    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this company should be treated as active."
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the company was deactivated (soft deleted)."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.nit})"
