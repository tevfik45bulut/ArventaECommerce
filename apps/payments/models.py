from django.db import models

from apps.common.models import BaseModel
from apps.orders.models import Order


class PaymentMethod(models.TextChoices):
    CREDIT_CARD = "credit_card", "Kredi Kartı"
    BANK_TRANSFER = "bank_transfer", "Havale / EFT"
    CASH_ON_DELIVERY = "cash_on_delivery", "Kapıda Ödeme"


class Payment(BaseModel):

    class Status(models.TextChoices):
        PENDING = "pending", "Bekliyor"
        SUCCESS = "success", "Başarılı"
        FAILED = "failed", "Başarısız"
        REFUNDED = "refunded", "İade"

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
    )

    provider = models.CharField(
        max_length=50,
        blank=True,
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.order.order_number


class PaymentLog(models.Model):

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="logs",
    )

    status = models.CharField(max_length=50)

    response = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment.order.order_number