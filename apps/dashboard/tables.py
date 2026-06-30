from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from django.db.models import Model


@dataclass(slots=True)
class TableColumn:
    """
    Dashboard tablo kolon tanımı.
    """

    field: str
    title: str
    searchable: bool = False
    sortable: bool = True
    default: Any = "-"

    def get_value(self, obj: Model) -> Any:
        """
        Objeden alan değerini güvenli şekilde döndürür.

        field örnekleri:

            name
            category__name
            brand__name
        """

        value = obj

        for attr in self.field.split("__"):
            value = getattr(value, attr, None)

            if value is None:
                return self.default

        if callable(value):
            value = value()

        if value in ("", None):
            return self.default

        return value


class DashboardTable:
    """
    Generic Dashboard tablo sınıfı.
    """

    columns: list[TableColumn] = []

    def __init__(self, queryset):
        self.queryset = queryset

    @property
    def headers(self):
        return self.columns

    @property
    def rows(self):
        data = []

        for obj in self.queryset:

            values = []

            for column in self.columns:
                values.append(column.get_value(obj))

            data.append(
                {
                    "object": obj,
                    "values": values,
                }
            )

        return data