from django.db import models
from django.conf import settings


class Taxpayer(models.Model):

    GENDER = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    MARITAL_STATUS = (
        ("Single", "Single"),
        ("Married", "Married"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=150)

    email = models.EmailField()

    mobile = models.CharField(max_length=10)

    pan_number = models.CharField(max_length=10, unique=True)

    aadhaar_number = models.CharField(max_length=12, unique=True)

    dob = models.DateField()

    gender = models.CharField(
        max_length=20,
        choices=GENDER
    )

    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS
    )

    occupation = models.CharField(max_length=100)

    annual_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name