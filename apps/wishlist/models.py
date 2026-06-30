from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.products.models import Product


class Wishlist(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist",
    )

    class Meta:
        verbose_name = "İstek Listesi"
        verbose_name_plural = "İstek Listesi"

    def __str__(self):
        return self.user.email


class WishlistItem(BaseModel):
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            "wishlist",
            "product",
        )
        verbose_name = "İstek Listesi Ürünü"
        verbose_name_plural = "İstek Listesi Ürünleri"

    def __str__(self):
        return self.product.name