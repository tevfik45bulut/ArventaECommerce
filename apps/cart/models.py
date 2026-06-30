from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.products.models import Product, ProductVariant


class Cart(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = "Sepet"
        verbose_name_plural = "Sepet"


class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = (
            "cart",
            "product",
            "variant",
        )

        verbose_name = "Sepet Ürünü"
        verbose_name_plural = "Sepet Ürünleri"

    @property
    def unit_price(self):
        if self.variant:
            return self.variant.price
        return self.product.price

    @property
    def total_price(self):
        return self.unit_price * self.quantity