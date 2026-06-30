from django.views.generic import DetailView, ListView

from .services import ProductService


class ProductListView(ListView):

    template_name = "products/list.html"

    context_object_name = "products"

    paginate_by = 12

    def get_queryset(self):

        return ProductService.products()


class ProductDetailView(DetailView):

    template_name = "products/detail.html"

    context_object_name = "product"

    slug_url_kwarg = "slug"

    def get_object(self):

        return ProductService.detail(
            self.kwargs["slug"]
        )