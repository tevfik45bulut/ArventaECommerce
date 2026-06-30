from django.contrib import admin

from .models import (
    Product,
    ProductAttribute,
    ProductAttributeValue,
    ProductImage,
    ProductReview,
    ProductTag,
    ProductVariant,
    ProductVariantValue,
)

class ProductVariantValueInline(admin.TabularInline):
    model = ProductVariantValue
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "sku",
        "price",
        "stock",
    )

    inlines = [
        ProductVariantValueInline,
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "category",
        "price",
        "stock",
        "is_active",
    )

    list_filter = (
        "category",
        "brand",
        "is_active",
    )

    search_fields = (
        "name",
        "sku",
    )

    filter_horizontal = (
        "tags",
    )

    inlines = [
        ProductImageInline,
    ]

admin.site.register(ProductTag)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(ProductReview)
admin.site.register(ProductVariantValue)