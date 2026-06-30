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
    ProductDocument,
    ProductSpecification,
    RelatedProduct,
    ProductSpecificationGroup,
)

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 0


@admin.register(ProductSpecificationGroup)
class ProductSpecificationGroupAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "name",
        "sort_order",
    )

    inlines = [
        ProductSpecificationInline,
    ]

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
admin.site.register(ProductDocument)
admin.site.register(RelatedProduct)