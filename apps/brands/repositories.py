from apps.common.repositories.base import BaseRepository

from .models import Brand


class BrandRepository(BaseRepository):

    model = Brand