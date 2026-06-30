from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .models import Wishlist


class WishlistView(LoginRequiredMixin, TemplateView):

    template_name = "wishlist/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        wishlist, _ = Wishlist.objects.get_or_create(
            user=self.request.user,
        )

        context["wishlist"] = wishlist

        return context