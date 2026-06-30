from apps.common.repositories.base import BaseRepository

from .models import Product


class ProductRepository(BaseRepository):

    model = Product

    @classmethod
    def list(cls):

        return (
            cls.model.objects
            .filter(is_active=True)
            .select_related(
                "category",
                "brand",
            )
            .prefetch_related(
                "images",
            )
        )