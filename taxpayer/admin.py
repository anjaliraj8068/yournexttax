from django.contrib import admin
from .models import Taxpayer


@admin.register(Taxpayer)
class TaxpayerAdmin(admin.ModelAdmin):

    list_display = (
        "full_name",
        "pan_number",
        "mobile",
        "annual_income",
    )

    search_fields = (
        "full_name",
        "pan_number",
    )