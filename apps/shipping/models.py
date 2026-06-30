from django.db import models

from apps.common.models import BaseModel


class ShippingCompany(BaseModel):
    name = models.CharField(max_length=150)

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    website = models.URLField(blank=True)

    tracking_url = models.URLField(blank=True)

    logo = models.ImageField(
        upload_to="shipping/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kargo Firması"
        verbose_name_plural = "Kargo Firması"


class ShippingMethod(BaseModel):
    company = models.ForeignKey(
        ShippingCompany,
        on_delete=models.CASCADE,
        related_name="methods",
    )

    name = models.CharField(max_length=150)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    free_shipping_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    estimated_days = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kargo Yöntemi"
        verbose_name_plural = "Kargo Yöntemi"