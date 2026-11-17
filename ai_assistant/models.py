from django.db import models
from django.conf import settings


class AIReport(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    total_income = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total_deduction = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    tax_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    ai_response = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.created_at.date()}"