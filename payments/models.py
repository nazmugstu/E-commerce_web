from django.db import models
from django.conf import settings
from core.models import Order

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Bkash', 'Bkash'),
        ('Nagad', 'Nagad'),
        ('Visa', 'Visa'),
        ('Mastercard', 'Mastercard'),
        ('SSLCommerz', 'SSLCommerz'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    currency = models.CharField(max_length=3, default='BDT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        username = self.user.username if self.user else "Guest"
        return f"Payment {self.transaction_id} by {username}"

    class Meta:
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['payment_status']),
        ]
