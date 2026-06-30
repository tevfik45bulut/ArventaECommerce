from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.brands.models import Brand
from apps.categories.models import Category
from apps.orders.models import Order
from apps.products.models import Product

User = get_user_model()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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