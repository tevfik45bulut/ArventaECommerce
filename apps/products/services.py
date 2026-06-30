from .repositories import ProductRepository


class ProductService:

    @staticmethod
    def products():

        return ProductRepository.list()

    @staticmethod
    def detail(slug):

        return ProductRepository.get(slug=slug)