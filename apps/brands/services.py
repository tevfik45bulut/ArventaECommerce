from .repositories import BrandRepository


class BrandService:

    @staticmethod
    def all():

        return BrandRepository.active()