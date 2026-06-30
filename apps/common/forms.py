from django import forms


class BaseForm(forms.ModelForm):
    class Meta:
        abstract = True