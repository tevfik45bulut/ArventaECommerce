from django.db import models
from django.utils.text import slugify


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SEOModel(models.Model):
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True


class SlugModel(models.Model):
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True

    def generate_slug(self, value):
        slug = slugify(value)
        model = self.__class__

        if not model.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            return slug

        index = 1

        while model.objects.filter(slug=f"{slug}-{index}").exclude(pk=self.pk).exists():
            index += 1

        return f"{slug}-{index}"


class BaseModel(
    TimeStampedModel,
    StatusModel,
):
    class Meta:
        abstract = True