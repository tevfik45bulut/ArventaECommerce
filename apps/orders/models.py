from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.products.models import Product, ProductVariant
from apps.shipping.models import ShippingMethod

class Order(BaseModel):

    class Status(models.TextChoices):
        PENDING = "pending", "Bekliyor"
        PROCESSING = "processing", "Hazırlanıyor"
        SHIPPED = "shipped", "Kargoda"
        DELIVERED = "delivered", "Teslim Edildi"
        CANCELLED = "cancelled", "İptal"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )

    order_number = models.CharField(
        max_length=30,
        unique=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    shipping_method = models.ForeignKey(
        ShippingMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    shipping_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return self.order_number
    
    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Sipariş"  


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    product_name = models.CharField(max_length=255)

    sku = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = "Sipariş Ürünü"
        verbose_name_plural = "Sipariş Ürünleri"   


class OrderAddress(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="address",
    )

    full_name = models.CharField(max_length=255)

    phone = models.CharField(max_length=20)

    city = models.CharField(max_length=100)

    district = models.CharField(max_length=100)

    address = models.TextField()

    postal_code = models.CharField(
        max_length=20,
        blank=True,
    )

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Sipariş Adresi"
        verbose_name_plural = "Sipariş Adresi"


class OrderStatusHistory(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="history",
    )

    status = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Sipariş Durum Geçmişi"
        verbose_name_plural = "Sipariş Durum Geçmişi"


class OrderNote(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    note = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Sipariş Notu"
        verbose_name_plural = "Sipariş Notları"