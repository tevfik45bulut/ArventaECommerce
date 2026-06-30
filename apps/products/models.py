from django.db import models
from django.urls import reverse

from apps.brands.models import Brand
from apps.categories.models import Category
from apps.common.models import BaseModel, SEOModel, SlugModel
from apps.common.utils import unique_slug


class Product(BaseModel, SEOModel, SlugModel):
    class ProductType(models.TextChoices):
        SIMPLE = "simple", "Basit"
        VARIABLE = "variable", "Varyantlı"
        DIGITAL = "digital", "Dijital"

    name = models.CharField(max_length=255)

    product_type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        default=ProductType.SIMPLE,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
    )

    sku = models.CharField(max_length=100, unique=True)

    barcode = models.CharField(
        max_length=100,
        blank=True,
    )

    short_description = models.TextField(blank=True)

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    compare_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["name"]
        verbose_name = "Ürün"
        verbose_name_plural = "Ürün"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)

        super().save(*args, **kwargs)