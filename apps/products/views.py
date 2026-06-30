from django.views.generic import DetailView, ListView

from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "products/list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(
            is_active=True,
        ).select_related(
            "category",
            "brand",
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True)
            .select_related(
                "brand",
                "category",
            )
            .prefetch_related(
                "images",
                "variants",
                "reviews",
                "specifications",
                "documents",
                "related_products__related_product",
            )
        )