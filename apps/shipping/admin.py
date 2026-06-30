from django.contrib import admin

from .models import ShippingCompany, ShippingMethod


class ShippingMethodInline(admin.TabularInline):
    model = ShippingMethod
    extra = 0


@admin.register(ShippingCompany)
class ShippingCompanyAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "is_active",
    )

    inlines = [
        ShippingMethodInline,
    ]