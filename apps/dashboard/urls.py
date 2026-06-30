from django.urls import path

from .views import (
    DashboardProductCreateView,
    DashboardProductDeleteView,
    DashboardProductDetailView,
    DashboardProductListView,
    DashboardProductUpdateView,
    DashboardView,
)

app_name = "dashboard"

urlpatterns = [
    path(
        "",
        DashboardView.as_view(),
        name="index",
    ),

    path(
        "products/",
        DashboardProductListView.as_view(),
        name="products",
    ),

    path(
        "products/create/",
        DashboardProductCreateView.as_view(),
        name="product_create",
    ),

    path(
        "products/<int:pk>/",
        DashboardProductDetailView.as_view(),
        name="product_detail",
    ),

    path(
        "products/<int:pk>/edit/",
        DashboardProductUpdateView.as_view(),
        name="product_update",
    ),

    path(
        "products/<int:pk>/delete/",
        DashboardProductDeleteView.as_view(),
        name="product_delete",
    ),
]