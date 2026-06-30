from django.apps import apps


class DashboardService:
    """
    Dashboard ortak servisleri.
    """

    @staticmethod
    def statistics():
        Product = apps.get_model("products", "Product")
        Category = apps.get_model("categories", "Category")
        Brand = apps.get_model("brands", "Brand")
        Order = apps.get_model("orders", "Order")

        return {
            "products": Product.objects.count(),
            "categories": Category.objects.count(),
            "brands": Brand.objects.count(),
            "orders": Order.objects.count(),
        }

    @staticmethod
    def latest_products(limit=10):
        Product = apps.get_model("products", "Product")

        return (
            Product.objects
            .select_related(
                "category",
                "brand",
            )
            .order_by("-id")[:limit]
        )

    @staticmethod
    def latest_orders(limit=10):
        Order = apps.get_model("orders", "Order")

        return (
            Order.objects
            .select_related(
                "user",
            )
            .order_by("-id")[:limit]
        )

    @staticmethod
    def dashboard_context():

        stats = DashboardService.statistics()

        stats["latest_products"] = (
            DashboardService.latest_products()
        )

        stats["latest_orders"] = (
            DashboardService.latest_orders()
        )

        return stats