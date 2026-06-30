from apps.common.repositories.base import BaseRepository

from .models import Category


class CategoryRepository(BaseRepository):

    model = Category