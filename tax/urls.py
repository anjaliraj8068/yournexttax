from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.tax_calculator,
        name="tax_calculator"
    ),
    path(
    "download/",
    views.download_tax_report,
    name="download_tax_report"
    ),

]