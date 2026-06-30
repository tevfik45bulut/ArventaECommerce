from .base import BasePaymentProvider


class ManualPaymentProvider(BasePaymentProvider):

    def pay(self, order):
        return True

    def refund(self, payment):
        return True