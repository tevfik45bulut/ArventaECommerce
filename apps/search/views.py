from django.db.models import Q
from django.views.generic import ListView

from apps.products.models import Product


class SearchView(ListView):

    model = Product

    template_name = "search/results.html"

    context_object_name = "products"

    def get_queryset(self):

        q = self.request.GET.get("q", "")

        return Product.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(short_description__icontains=q)
        ).distinct()