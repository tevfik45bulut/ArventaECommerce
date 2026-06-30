from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from apps.dashboard.mixins import DashboardAccessMixin
from apps.products.models import Product

from django.views.generic import TemplateView

from apps.brands.models import Brand
from apps.categories.models import Category
from apps.orders.models import Order

from django.views.generic import TemplateView

from apps.brands.models import Brand
from apps.categories.models import Category
from apps.orders.models import Order

from apps.brands.models import Brand
from apps.categories.models import Category
from apps.dashboard.filters import ProductFilter

from django.db.models import Q


class DashboardView(DashboardAccessMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["product_count"] = Product.objects.count()
        context["category_count"] = Category.objects.count()
        context["brand_count"] = Brand.objects.count()
        context["order_count"] = Order.objects.count()

        context["latest_products"] = (
            Product.objects
            .select_related("category", "brand")
            .order_by("-id")[:10]
        )

        context["latest_orders"] = (
            Order.objects
            .order_by("-id")[:10]
        )

        return context


class DashboardProductListView(
    DashboardAccessMixin,
    ListView,
):
    model = Product

    template_name = "dashboard/products/list.html"

    context_object_name = "products"

    paginate_by = 20

    filterset_class = ProductFilter

    def get_queryset(self):

        queryset = (
            Product.objects
            .select_related(
                "category",
                "brand",
            )
            .order_by("-id")
        )

        queryset = self.filterset_class(
            self.request,
            queryset,
        ).filter_queryset()

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["title"] = "Ürünler"

        context["search"] = self.request.GET.get(
            "q",
            "",
        )

        context["categories"] = Category.objects.all()

        context["brands"] = Brand.objects.all()

        context["selected_category"] = self.request.GET.get(
            "category",
            "",
        )

        context["selected_brand"] = self.request.GET.get(
            "brand",
            "",
        )

        context["selected_status"] = self.request.GET.get(
            "is_active",
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
    

class DashboardProductDetailView(
    DashboardAccessMixin,
    DetailView,
):
    model = Product

    template_name = "dashboard/products/detail.html"

    context_object_name = "product"

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

    success_url = reverse_lazy("dashboard:products")

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

    success_url = reverse_lazy("dashboard:products")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["title"] = "Ürün Güncelle"

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

    success_url = reverse_lazy("dashboard:products")

    context_object_name = "product"

    def form_valid(self, form):
        messages.success(
            self.request,
            "Ürün başarıyla silindi.",
        )

        return super().form_valid(form)