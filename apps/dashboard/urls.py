from django.urls import path

from .views import DashboardView, DashboardProductListView

app_name = "dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="index"),
    path("products/", DashboardProductListView.as_view(), name="products",
),
]