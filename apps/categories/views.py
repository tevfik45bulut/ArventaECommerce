from django.views.generic import DetailView, ListView

from .models import Category


class CategoryListView(ListView):
    model = Category
    template_name = "categories/list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(is_active=True, parent=None)


class CategoryDetailView(DetailView):
    model = Category
    template_name = "categories/detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"