from django.urls import path

from .views import BrandDetailView, BrandListView

app_name = "brands"

urlpatterns = [
    path("", BrandListView.as_view(), name="list"),
    path("<slug:slug>/", BrandDetailView.as_view(), name="detail"),
]