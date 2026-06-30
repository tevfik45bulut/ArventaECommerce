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

    barcode = models.CharField(max_length=100, blank=True)

    short_description = models.TextField(blank=True)

    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    compare_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    stock = models.PositiveIntegerField(default=0)

    tags = models.ManyToManyField(
        "ProductTag",
        blank=True,
        related_name="products",
    )

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


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(upload_to="products/")

    alt = models.CharField(max_length=255, blank=True)

    is_cover = models.BooleanField(default=False)

    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Ürün Görseli"
        verbose_name_plural = "Ürün Görselleri"


class ProductTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Ürün Etiketi"
        verbose_name_plural = "Ürün Etiketleri"


class ProductAttribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Ürün Niteliği"
        verbose_name_plural = "Ürün Nitelikleri"


class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE,
        related_name="values",
    )

    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"

    class Meta:
        verbose_name = "Ürün Nitelik Değeri"
        verbose_name_plural = "Ürün Nitelik Değerleri"


class ProductVariant(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    barcode = models.CharField(
        max_length=100,
        blank=True,
    )

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

    image = models.ForeignKey(
        "ProductImage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

    class Meta:
        verbose_name = "Ürün Varyantı"
        verbose_name_plural = "Ürün Varyantları"


class ProductVariantValue(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="variant_values",
    )

    attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE,
    )

    value = models.ForeignKey(
        ProductAttributeValue,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = (
            "variant",
            "attribute",
        )

    def __str__(self):
        return f"{self.variant.sku} - {self.attribute.name}: {self.value.value}"
    
    class Meta:
        verbose_name = "Ürün Varyant Değeri"
        verbose_name_plural = "Ürün Varyant Değerleri"


class ProductReview(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    name = models.CharField(max_length=100)

    rating = models.PositiveSmallIntegerField()

    comment = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Ürün İncelemesi"
        verbose_name_plural = "Ürün İncelemeleri"


class ProductSpecificationGroup(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="specification_groups",
    )

    name = models.CharField(max_length=150)

    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Ürün Özellik Grubu"
        verbose_name_plural = "Ürün Özellik Grupları"

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    group = models.ForeignKey(
        ProductSpecificationGroup,
        on_delete=models.CASCADE,
        related_name="specifications",
    )

    title = models.CharField(max_length=150)

    value = models.CharField(max_length=255)

    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Ürün Nitelik Değeri"
    def __str__(self):
        return f"{self.title}: {self.value}"


class ProductDocument(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="documents",
    )

    title = models.CharField(max_length=150)

    file = models.FileField(upload_to="products/documents/")

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Ürün Belgesi"
        verbose_name_plural = "Ürün Belgeleri"


class RelatedProduct(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="related_products",
    )

    related_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="related_to",
    )

    class Meta:
        unique_together = (
            "product",
            "related_product",
        )
        verbose_name = "İlgili Ürün"
        verbose_name_plural = "İlgili Ürünler"

    def __str__(self):
        return f"{self.product} -> {self.related_product}"