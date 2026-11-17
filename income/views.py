from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Income
from .forms import IncomeForm
from notifications.services import create_notification


@login_required
def income_list(request):

    incomes = Income.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "income/income_list.html",
        {
            "incomes": incomes
        }
    )


@login_required
def add_income(request):

    if request.method == "POST":

        form = IncomeForm(request.POST)

        if form.is_valid():

            income = form.save(commit=False)

            income.user = request.user

            income.save()
            create_notification(

                request.user,

                "Income Added",

                f"₹{income.amount} income added successfully.",

                "success"

            )

            messages.success(
                request,
                "Income added successfully."
            )

            return redirect("income_list")

    else:

        form = IncomeForm()

    return render(
        request,
        "income/add_income.html",
        {
            "form": form
        }
    )
@login_required
def edit_income(request, pk):

    income = Income.objects.get(
        id=pk,
        user=request.user
    )

    if request.method == "POST":

        form = IncomeForm(
            request.POST,
            instance=income
        )

        if form.is_valid():

        
            updated_income = form.save()

            create_notification(

                request.user,

                "Income Updated",

                f"Income updated to ₹{updated_income.amount}.",

                "primary"

            )

            messages.success(
                request,
                "Income updated successfully."
            )

            return redirect("income_list")

    else:

        form = IncomeForm(instance=income)

    return render(
        request,
        "income/add_income.html",
        {
            "form": form
        }
    )


@login_required
def delete_income(request, pk):
    
    income = Income.objects.get(
        id=pk,
        user=request.user
    )
    amount = income.amount

    income.delete()

    create_notification(
        request.user,
        "Income Deleted",
        f"₹{amount} income deleted successfully.",
        "warning"
    )

    messages.success(
        request,
        "Income deleted successfully."
    )

    return redirect("income_list")