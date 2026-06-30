from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class TableColumn:
    """
    Dashboard tablo kolon tanımı.
    """

    field: str
    title: str

    sortable: bool = True

    searchable: bool = False

    css_class: str = ""

    default: Any = "-"

    formatter: callable | None = None

    def value(self, obj):

        value = obj

        for part in self.field.split("__"):

            value = getattr(value, part, None)

            if value is None:
                return self.default

        if callable(value):
            value = value()

        if value in ("", None):
            value = self.default

        if self.formatter:
            return self.formatter(value)

        return value


class DashboardTable:
    """
    Generic Dashboard Table
    """

    columns = []

    def __init__(self, queryset):

        self.queryset = queryset

    @property
    def headers(self):

        return self.columns

    @property
    def rows(self):

        rows = []

        for obj in self.queryset:

            row = {
                "object": obj,
                "columns": [],
            }

            for column in self.columns:

                row["columns"].append(
                    column.value(obj)
                )

            rows.append(row)

        return rows


class ProductTable(DashboardTable):

    columns = [

        TableColumn(
            "id",
            "ID",
        ),

        TableColumn(
            "name",
            "Ürün",
            searchable=True,
        ),

        TableColumn(
            "sku",
            "SKU",
            searchable=True,
        ),

        TableColumn(
            "category__name",
            "Kategori",
        ),

        TableColumn(
            "brand__name",
            "Marka",
        ),

        TableColumn(
            "price",
            "Fiyat",
        ),

        TableColumn(
            "stock",
            "Stok",
        ),

        TableColumn(
            "is_active",
            "Durum",
            formatter=lambda value: (
                "Aktif"
                if value
                else "Pasif"
            ),
        ),

    ]