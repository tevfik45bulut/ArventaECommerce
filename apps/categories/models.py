from django.db import models
from django.urls import reverse

from apps.common.models import BaseModel, SEOModel, SlugModel
from apps.common.utils import unique_slug


class Category(BaseModel, SEOModel, SlugModel):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
    )

    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("categories:detail", args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)

        super().save(*args, **kwargs)