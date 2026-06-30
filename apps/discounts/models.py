from django.db import models

from apps.common.models import BaseModel


class Coupon(BaseModel):
    code = models.CharField(
        max_length=50,
        unique=True,
    )

    discount_percent = models.PositiveIntegerField(default=0)

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    minimum_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    usage_limit = models.PositiveIntegerField(default=1)

    used_count = models.PositiveIntegerField(default=0)

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = "Kupon"
        verbose_name_plural = "Kupon"