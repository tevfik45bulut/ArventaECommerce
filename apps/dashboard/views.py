from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from apps.dashboard.mixins import DashboardAccessMixin
from apps.products.models import Product


class DashboardProductListView(DashboardAccessMixin, ListView):
    model = Product
    template_name = "dashboard/products/list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        queryset = (
            Product.objects
            .select_related(
                "category",
                "brand",
            )
            .order_by("-id")
        )

        q = self.request.GET.get("q")

        if q:
            queryset = queryset.filter(
                name__icontains=q,
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Ürünler"

        context["search"] = self.request.GET.get(
            "q",
            "",
        )

        return context


class DashboardProductDetailView(
    DashboardAccessMixin,
    DetailView,
):
    model = Product
    template_name = "dashboard/products/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = self.object.name

        return context


class DashboardProductCreateView(
    DashboardAccessMixin,
    CreateView,
):
    model = Product

    fields = "__all__"

    template_name = "dashboard/products/form.html"

    success_url = reverse_lazy(
        "dashboard:products"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Yeni Ürün"

        return context

    def form_valid(self, form):
        messages.success(
            self.request,
            "Ürün başarıyla oluşturuldu.",
        )

        return super().form_valid(form)


class DashboardProductUpdateView(
    DashboardAccessMixin,
    UpdateView,
):
    model = Product

    fields = "__all__"

    template_name = "dashboard/products/form.html"

    success_url = reverse_lazy(
        "dashboard:products"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Ürün Düzenle"

        return context

    def form_valid(self, form):
        messages.success(
            self.request,
            "Ürün başarıyla güncellendi.",
        )

        return super().form_valid(form)


class DashboardProductDeleteView(
    DashboardAccessMixin,
    DeleteView,
):
    model = Product

    template_name = "dashboard/products/delete.html"

    success_url = reverse_lazy(
        "dashboard:products"
    )

    def form_valid(self, form):
        messages.success(
            self.request,
            "Ürün başarıyla silindi.",
        )

        return super().form_valid(form)