from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic import TemplateView

from apps.brands.models import Brand
from apps.categories.models import Category
from apps.dashboard.crud import CrudService
from apps.dashboard.crud import build_context
from apps.dashboard.crud import registry
from apps.dashboard.mixins import DashboardAccessMixin
from apps.dashboard.services import DashboardService
from apps.orders.models import Order
from apps.products.models import Product

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(DashboardService.statistics())

        context["product_count"] = Product.objects.count()
        context["category_count"] = Category.objects.count()
        context["brand_count"] = Brand.objects.count()
        context["order_count"] = Order.objects.count()
        context["user_count"] = User.objects.count()

        context["last_orders"] = (
            Order.objects.select_related("user")
            .order_by("-created_at")[:10]
        )

        return context


class GenericDashboardListView(
    DashboardAccessMixin,
    ListView,
):
    crud_name = None

    template_name = "dashboard/crud/list.html"

    context_object_name = "objects"

    paginate_by = 20

    config = None

    def dispatch(self, request, *args, **kwargs):
        DashboardService.register_cruds()

        self.config = registry.get(self.crud_name)

        self.model = self.config.model

        self.paginate_by = self.config.paginate_by

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = CrudService.queryset(self.config)

        keyword = self.request.GET.get("q", "").strip()

        queryset = CrudService.search(
            queryset=queryset,
            config=self.config,
            keyword=keyword,
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            build_context(
                config=self.config,
                queryset=context["object_list"],
                page_obj=context.get("page_obj"),
            )
        )

        context["search"] = self.request.GET.get("q", "")

        return context


class DashboardProductListView(GenericDashboardListView):
    crud_name = "products"

    template_name = "dashboard/products/list.html"

    def get_queryset(self):
        queryset = DashboardService.product_queryset()

        keyword = self.request.GET.get("q", "").strip()

        if keyword:
            queryset = queryset.filter(
                Q(name__icontains=keyword)
                | Q(sku__icontains=keyword)
                | Q(category__name__icontains=keyword)
                | Q(brand__name__icontains=keyword)
            )

        return queryset