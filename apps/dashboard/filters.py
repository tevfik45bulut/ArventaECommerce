from __future__ import annotations

from django.db.models import Q


class DashboardFilter:
    """
    Generic Dashboard filtre sınıfı.
    """

    search_fields = ()

    filter_fields = ()

    def __init__(self, request, queryset):
        self.request = request
        self.queryset = queryset

    def filter_queryset(self):

        queryset = self.queryset

        queryset = self.apply_search(queryset)

        queryset = self.apply_filters(queryset)

        return queryset

    def apply_search(self, queryset):

        keyword = self.request.GET.get(
            "q",
            "",
        ).strip()

        if not keyword:
            return queryset

        if not self.search_fields:
            return queryset

        query = Q()

        for field in self.search_fields:

            query |= Q(
                **{
                    f"{field}__icontains": keyword
                }
            )

        return queryset.filter(query)

    def apply_filters(self, queryset):

        for field in self.filter_fields:

            value = self.request.GET.get(field)

            if value in ("", None):
                continue

            queryset = queryset.filter(
                **{
                    field: value
                }
            )

        return queryset


class ProductFilter(DashboardFilter):

    search_fields = (
        "name",
        "sku",
        "category__name",
        "brand__name",
    )

    filter_fields = (
        "category",
        "brand",
        "is_active",
    )