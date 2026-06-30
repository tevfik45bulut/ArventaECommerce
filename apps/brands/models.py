from django.db import models
from django.urls import reverse

from apps.common.models import BaseModel, SEOModel, SlugModel
from apps.common.utils import unique_slug


class Brand(BaseModel, SEOModel, SlugModel):
    name = models.CharField(max_length=150)

    logo = models.ImageField(
        upload_to="brands/",
        blank=True,
        null=True,
    )

    description = models.TextField(blank=True)

    website = models.URLField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Marka"
        verbose_name_plural = "Marka"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("brands:detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)

        super().save(*args, **kwargs)