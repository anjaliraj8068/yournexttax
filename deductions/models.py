from django.db import models
from django.conf import settings


class Deduction(models.Model):

    SECTION = (

        ("80C", "80C"),
        ("80D", "80D"),
        ("80G", "80G"),
        ("NPS", "NPS"),
        ("Home Loan", "Home Loan"),
        ("Education Loan", "Education Loan"),

    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    section = models.CharField(
        max_length=30,
        choices=SECTION
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # 👇 Add here
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

        return self.section