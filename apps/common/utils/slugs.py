from django.utils.text import slugify


def unique_slug(instance, value):
    slug = slugify(value)

    Model = instance.__class__

    if not Model.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        return slug

    number = 1

    while Model.objects.filter(
        slug=f"{slug}-{number}"
    ).exclude(pk=instance.pk).exists():
        number += 1

    return f"{slug}-{number}"