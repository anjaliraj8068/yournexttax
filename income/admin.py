from django.contrib import admin
from .models import Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "income_type",
        "amount",
        "financial_year",
    )

    list_filter = (
        "income_type",
        "financial_year",
    )

    search_fields = (
        "financial_year",
        "user__username",
    )