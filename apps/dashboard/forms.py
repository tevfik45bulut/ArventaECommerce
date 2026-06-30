from django import forms
from django.forms import ModelForm


class SearchForm(forms.Form):
    """
    Dashboard ortak arama formu.
    """

    q = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ara...",
                "autocomplete": "off",
            }
        ),
    )


class DashboardModelForm(ModelForm):
    """
    Dashboard için ortak ModelForm.

    Bootstrap 5 sınıflarını otomatik uygular.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            widget = field.widget

            if isinstance(widget, forms.CheckboxInput):

                widget.attrs["class"] = (
                    widget.attrs.get("class", "")
                    + " form-check-input"
                ).strip()

            elif isinstance(widget, forms.Select):

                widget.attrs["class"] = (
                    widget.attrs.get("class", "")
                    + " form-select"
                ).strip()

            elif isinstance(widget, forms.SelectMultiple):

                widget.attrs["class"] = (
                    widget.attrs.get("class", "")
                    + " form-select"
                ).strip()

            elif isinstance(widget, forms.ClearableFileInput):

                widget.attrs["class"] = (
                    widget.attrs.get("class", "")
                    + " form-control"
                ).strip()

            elif isinstance(widget, forms.FileInput):

                widget.attrs["class"] = (
                    widget.attrs.get("class", "")
                    + " form-control"
                ).strip()

            elif isinstance(widget, forms.Textarea):

                widget.attrs["class"] = (
                    widget.attrs.get("class", "")
                    + " form-control"
                ).strip()

                widget.attrs.setdefault("rows", 4)

            else:

                widget.attrs["class"] = (
                    widget.attrs.get("class", "")
                    + " form-control"
                ).strip()


class DashboardFormFactory:
    """
    Generic Dashboard Form Factory

    Örnek:

        ProductForm = DashboardFormFactory.create(
            Product,
            fields="__all__",
        )
    """

    @staticmethod
    def create(
        model,
        *,
        fields="__all__",
        exclude=None,
        widgets=None,
        labels=None,
        help_texts=None,
    ):

        widgets = widgets or {}
        labels = labels or {}
        help_texts = help_texts or {}

        class Meta:

            model = model

            fields = fields

            exclude = exclude

            widgets = widgets

            labels = labels

            help_texts = help_texts

        return type(
            f"{model.__name__}Form",
            (DashboardModelForm,),
            {
                "Meta": Meta,
            },
        )