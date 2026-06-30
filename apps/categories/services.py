from .repositories import CategoryRepository


class CategoryService:

    @staticmethod
    def all():

        return CategoryRepository.active()