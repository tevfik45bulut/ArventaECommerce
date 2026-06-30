from django.contrib import admin

from .models import Payment, PaymentLog


class PaymentLogInline(admin.TabularInline):
    model = PaymentLog
    extra = 0


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "method",
        "status",
        "amount",
        "paid_at",
    )

    list_filter = (
        "status",
        "method",
    )

    inlines = [
        PaymentLogInline,
    ]