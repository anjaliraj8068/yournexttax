from django import forms
from .models import Taxpayer


class TaxpayerForm(forms.ModelForm):

    class Meta:

        model = Taxpayer

        exclude = ("user",)


        widgets = {

            "dob": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs["class"] = "form-control"