from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.db.models import Q
from django.db.models import QuerySet


@dataclass(slots=True)
class FilterField:
    """
    Dashboard filtre alanı.

    field:
        Model alanı

    lookup:
        Django lookup
        (icontains, exact, gte...)

    query_name:
        GET parametresi.
    """

    field: str

    query_name: str

    lookup: str = "exact"

    empty_value: Any = ""

    def apply(
        self,
        queryset: QuerySet,
        value: Any,
    ) -> QuerySet:

        if value in (
            None,
            "",
            self.empty_value,
        ):
            return queryset

        return queryset.filter(
            **{
                f"{self.field}__{self.lookup}": value
            }
        )


class SearchFilter:
    """
    Çok alanlı arama.
    """

    def __init__(
        self,
        *fields: str,
    ):

        self.fields = fields

    def apply(
        self,
        queryset: QuerySet,
        keyword: str,
    ) -> QuerySet:

        keyword = keyword.strip()

        if not keyword:
            return queryset

        query = Q()

        for field in self.fields:

            query |= Q(
                **{
                    f"{field}__icontains": keyword
                }
            )

        return queryset.filter(query)


class DashboardFilterSet:
    """
    Generic Dashboard filtre sınıfı.
    """

    search = None

    filters: list[FilterField] = []

    def __init__(
        self,
        request,
        queryset,
    ):

        self.request = request

        self.queryset = queryset

    def filter_queryset(self):

        queryset = self.queryset

        if self.search:

            queryset = self.search.apply(
                queryset,
                self.request.GET.get(
                    "q",
                    "",
                ),
            )

        for filter_field in self.filters:

            queryset = filter_field.apply(
                queryset,
                self.request.GET.get(
                    filter_field.query_name,
                ),
            )

        return queryset