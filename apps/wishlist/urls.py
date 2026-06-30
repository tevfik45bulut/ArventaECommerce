from django.urls import path

from .views import WishlistView

app_name = "wishlist"

urlpatterns = [
    path(
        "favoriler/",
        WishlistView.as_view(),
        name="list",
    ),
]