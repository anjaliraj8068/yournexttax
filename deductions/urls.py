from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.deduction_list,
        name="deduction_list"
    ),

    path(
        "add/",
        views.add_deduction,
        name="add_deduction"
    ),

    path(
        "edit/<int:pk>/",
        views.edit_deduction,
        name="edit_deduction"
    ),

    path(
        "delete/<int:pk>/",
        views.delete_deduction,
        name="delete_deduction"
    ),

]