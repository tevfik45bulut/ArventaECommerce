from django.contrib import admin

from .models import (
    Order,
    OrderAddress,
    OrderItem,
    OrderNote,
    OrderStatusHistory,
)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0


class OrderNoteInline(admin.TabularInline):
    model = OrderNote
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "user",
        "status",
        "total",
        "created_at",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "order_number",
    )

    inlines = [
        OrderItemInline,
        OrderHistoryInline,
        OrderNoteInline,
    ]


admin.site.register(OrderAddress)