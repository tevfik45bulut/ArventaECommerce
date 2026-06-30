from abc import ABC, abstractmethod


class BasePaymentProvider(ABC):

    @abstractmethod
    def pay(self, order):
        pass

    @abstractmethod
    def refund(self, payment):
        pass