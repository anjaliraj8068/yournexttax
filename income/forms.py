from django import forms
from .models import Income

FINANCIAL_YEARS = (
    ("2023-24", "2023-24"),
    ("2024-25", "2024-25"),
    ("2025-26", "2025-26"),
    ("2026-27", "2026-27"),
)

class IncomeForm(forms.ModelForm):

    class Meta:
        model = Income
        exclude = ("user",)
        widgets = {
            "financial_year": forms.Select(choices=FINANCIAL_YEARS)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"