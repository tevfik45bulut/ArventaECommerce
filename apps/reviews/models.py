from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.products.models import Product


class Review(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="customer_reviews",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    rating = models.PositiveSmallIntegerField()

    title = models.CharField(
        max_length=200,
        blank=True,
    )

    comment = models.TextField()

    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        unique_together = (
            "product",
            "user",
        )
        verbose_name = "Ürün Yorumu"
        verbose_name_plural = "Ürün Yorumları"

    def __str__(self):
        return f"{self.product} ({self.rating})"