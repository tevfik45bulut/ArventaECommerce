from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class DashboardAccessMixin(LoginRequiredMixin):
    """
    Dashboard erişim kontrolü.

    Kullanıcının giriş yapmış olmasını ve
    staff yetkisine sahip olmasını zorunlu kılar.
    """

    login_url = "accounts:login"

    permission_denied_message = (
        "Bu sayfaya erişim yetkiniz bulunmamaktadır."
    )

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_staff:
            raise PermissionDenied(
                self.permission_denied_message
            )

        return super().dispatch(
            request,
            *args,
            **kwargs,
        )


class DashboardListMixin:
    """
    Dashboard liste ekranları için ortak özellikler.
    """

    paginate_by = 20

    ordering = ("-id",)

    search_fields = ()

    search_param = "q"

    def get_search_query(self):
        return self.request.GET.get(
            self.search_param,
            "",
        ).strip()

    def get_ordering(self):
        return self.ordering

    def get_paginate_by(self, queryset):
        return self.paginate_by


class DashboardSuccessMessageMixin:
    """
    CRUD ekranları için ortak başarı mesajı.
    """

    success_message = None

    def form_valid(self, form):
        from django.contrib import messages

        response = super().form_valid(form)

        if self.success_message:
            messages.success(
                self.request,
                self.success_message,
            )

        return response