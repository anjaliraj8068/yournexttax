from django.db import models
from django.conf import settings


class Income(models.Model):

    INCOME_TYPE = (

        ("Salary", "Salary"),

        ("Business", "Business"),

        ("House Property", "House Property"),

        ("Capital Gain", "Capital Gain"),

        ("Other", "Other"),

    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    income_type = models.CharField(
        max_length=30,
        choices=INCOME_TYPE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    financial_year = models.CharField(
        max_length=20
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.income_type}"