from django.views.generic import DetailView, ListView

from .models import Brand


class BrandListView(ListView):
    model = Brand
    template_name = "brands/list.html"
    context_object_name = "brands"

    def get_queryset(self):
        return Brand.objects.filter(is_active=True)


class BrandDetailView(DetailView):
    model = Brand
    template_name = "brands/detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"