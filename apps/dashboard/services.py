from apps.brands.models import Brand
from apps.categories.models import Category
from apps.orders.models import Order
from apps.products.models import Product

from .crud import CrudColumn
from .crud import CrudConfig
from .crud import registry


class DashboardService:

    _crud_registered = False

    @staticmethod
    def statistics():
        """
        Dashboard ana sayfa istatistikleri.
        """

        return {
            "products": Product.objects.count(),
            "categories": Category.objects.count(),
            "brands": Brand.objects.count(),
            "orders": Order.objects.count(),
        }

    @classmethod
    def register_cruds(cls):
        """
        Generic CRUD tanımlarını sisteme yükler.

        Birden fazla kez çağrılsa bile tekrar kayıt oluşturmaz.
        """

        if cls._crud_registered:
            return

        registry.register(
            CrudConfig(
                name="products",
                model=Product,
                title="Ürünler",
                columns=[
                    CrudColumn("id", "ID"),
                    CrudColumn("name", "Ürün", searchable=True),
                    CrudColumn("sku", "SKU", searchable=True),
                    CrudColumn("category__name", "Kategori"),
                    CrudColumn("brand__name", "Marka"),
                    CrudColumn("price", "Fiyat"),
                    CrudColumn("stock", "Stok"),
                    CrudColumn("is_active", "Aktif"),
                ],
                search_fields=[
                    "name",
                    "sku",
                    "category__name",
                    "brand__name",
                ],
                ordering=("-id",),
                paginate_by=20,
            )
        )

        cls._crud_registered = True

    @staticmethod
    def product_queryset():
        """
        Products için ortak queryset.

        İleride CrudConfig içerisine taşınacaktır.
        """

        return (
            Product.objects
            .select_related(
                "category",
                "brand",
            )
            .order_by("-id")
        )