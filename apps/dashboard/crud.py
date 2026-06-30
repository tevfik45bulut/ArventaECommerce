from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from django.db.models import Model
from django.db.models import Q
from django.db.models import QuerySet


@dataclass(slots=True)
class CrudColumn:
    field: str
    label: str
    searchable: bool = False
    sortable: bool = True
    default: Any = "-"

    def resolve(self, obj: Model):

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


@dataclass(slots=True)
class CrudConfig:

    name: str

    model: type[Model]

    title: str

    columns: list[CrudColumn]

    search_fields: list[str] = field(default_factory=list)

    ordering: tuple[str, ...] = ("-id",)

    paginate_by: int = 20


class CrudRegistry:

    def __init__(self):
        self._items: dict[str, CrudConfig] = {}

    def register(self, config: CrudConfig):

        key = config.name.lower()

        if key in self._items:
            raise ValueError(f'"{config.name}" already registered.')

        self._items[key] = config

    def get(self, name: str):
        return self._items[name.lower()]

    def all(self):
        return self._items.values()


registry = CrudRegistry()


class CrudService:

    @staticmethod
    def queryset(config: CrudConfig):

        return (
            config.model.objects.all()
            .order_by(*config.ordering)
        )

    @staticmethod
    def search(
        queryset: QuerySet,
        config: CrudConfig,
        keyword: str,
    ):

        keyword = keyword.strip()

        if not keyword:
            return queryset

        if not config.search_fields:
            return queryset

        query = Q()

        for field in config.search_fields:
            query |= Q(
                **{
                    f"{field}__icontains": keyword,
                }
            )

        return queryset.filter(query)

    @staticmethod
    def rows(
        queryset: QuerySet,
        config: CrudConfig,
    ):

        rows = []

        for obj in queryset:

            values = []

            for column in config.columns:
                values.append(column.resolve(obj))

            rows.append(
                {
                    "object": obj,
                    "values": values,
                }
            )

        return rows


def build_context(
    *,
    config: CrudConfig,
    queryset,
    page_obj=None,
):
    """
    Generic CRUD template context.
    """

    return {
        "crud": config,
        "title": config.title,
        "columns": config.columns,
        "rows": CrudService.rows(
            queryset=queryset,
            config=config,
        ),
        "page_obj": page_obj,
        "paginate_by": config.paginate_by,
    }