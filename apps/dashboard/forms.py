from django import forms
from django.forms import ModelForm


class SearchForm(forms.Form):
    """
    Dashboard liste ekranlarında ortak arama formu.
    """

    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ara...",
            }
        ),
    )


class DashboardModelForm(ModelForm):
    """
    Generic Dashboard ModelForm.

    Bootstrap sınıflarını otomatik uygular.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            widget = field.widget

            if isinstance(
                widget,
                (
                    forms.CheckboxInput,
                    forms.CheckboxSelectMultiple,
                ),
            ):
                css = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{css} form-check-input"
                ).strip()

            elif isinstance(
                widget,
                (
                    forms.Select,
                    forms.SelectMultiple,
                ),
            ):
                css = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{css} form-select"
                ).strip()

            else:
                css = widget.attrs.get("class", "")
                widget.attrs["class"] = (
                    f"{css} form-control"
                ).strip()


class DashboardFormFactory:
    """
    Model bazlı ModelForm üreticisi.

    Örnek:

        ProductForm = DashboardFormFactory.create(
            Product,
            fields="__all__",
        )
    """

    @staticmethod
    def create(
        model,
        fields="__all__",
        exclude=None,
        widgets=None,
        labels=None,
        help_texts=None,
    ):
        widgets = widgets or {}
        labels = labels or {}
        help_texts = help_texts or {}

        meta = type(
            "Meta",
            (),
            {
                "model": model,
                "fields": fields,
                "exclude": exclude,
                "widgets": widgets,
                "labels": labels,
                "help_texts": help_texts,
            },
        )

        return type(
            f"{model.__name__}DashboardForm",
            (DashboardModelForm,),
            {
                "Meta": meta,
            },
        )