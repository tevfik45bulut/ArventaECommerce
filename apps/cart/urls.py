from django.urls import path

from .views import CartView

app_name = "cart"

urlpatterns = [
    path("sepet/", CartView.as_view(), name="detail"),
]