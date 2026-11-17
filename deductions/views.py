from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Deduction
from .forms import DeductionForm
from notifications.services import create_notification


@login_required
def deduction_list(request):

    deductions = Deduction.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "deductions/deduction_list.html",
        {
            "deductions": deductions
        }
    )


@login_required
def add_deduction(request):

    if request.method == "POST":

        form = DeductionForm(request.POST)

        if form.is_valid():

            deduction = form.save(commit=False)

            deduction.user = request.user

            deduction.save()
            create_notification(

                request.user,

                "Deduction Added",

                f"₹{deduction.amount} deduction added successfully.",

                "success"

            )

            messages.success(
                request,
                "Deduction added successfully."
            )

            return redirect("deduction_list")

    else:

        form = DeductionForm()

    return render(
        request,
        "deductions/add_deduction.html",
        {
            "form": form
        }
    )


@login_required
def edit_deduction(request, pk):

    deduction = get_object_or_404(
        Deduction,
        id=pk,
        user=request.user
    )

    if request.method == "POST":

        form = DeductionForm(
            request.POST,
            instance=deduction
        )

        if form.is_valid():

            
            updated_deduction = form.save()

            create_notification(

                request.user,

                "Deduction Updated",

                f"Deduction updated to ₹{updated_deduction.amount}.",

                "primary"

            )

            messages.success(
                request,
                "Deduction updated successfully."
            )

            return redirect("deduction_list")

    else:

        form = DeductionForm(instance=deduction)

    return render(
        request,
        "deductions/add_deduction.html",
        {
            "form": form
        }
    )


@login_required
def delete_deduction(request, pk):

    deduction = get_object_or_404(
        Deduction,
        id=pk,
        user=request.user
    )
    amount = deduction.amount

    deduction.delete()
    
    create_notification(

        request.user,

        "Deduction Deleted",

        f"Deduction ₹{amount} deleted successfully.",

        "danger"

    )
    messages.success(
        request,
        "Deduction deleted successfully."
    )

    return redirect("deduction_list")