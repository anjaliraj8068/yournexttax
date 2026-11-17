from decimal import Decimal

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from income.models import Income
from deductions.models import Deduction
from django.http import FileResponse

from notifications.models import Notification
from .pdf_generator import generate_tax_pdf
from notifications.services import create_notification, generate_notifications
from .utils import calculate_tax_summary

@login_required
def tax_calculator(request):

    # -----------------------------
    # Total Income
    # -----------------------------
    total_income = (
        Income.objects.filter(
            user=request.user
        ).aggregate(
            Sum("amount")
        )["amount__sum"] or Decimal("0")
    )
   
    # -----------------------------
    # Total Deduction
    # -----------------------------
    total_deduction = (
        Deduction.objects.filter(
            user=request.user
        ).aggregate(
            Sum("amount")
        )["amount__sum"] or Decimal("0")
    )

    # -----------------------------
    # Calculate Tax Summary
    # -----------------------------
    summary = calculate_tax_summary(total_income, total_deduction)

    # -----------------------------
    # Generate Notifications
    # -----------------------------
    generate_notifications(
        request.user,
        total_income,
        total_deduction
    )
    
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    # -----------------------------
    # Context
    # -----------------------------
    context = summary
    context["notifications"] = notifications

    return render(
        request,
        "tax/tax_calculator.html",
        context
    )

@login_required
def download_tax_report(request):

    total_income = (
        Income.objects.filter(user=request.user)
        .aggregate(Sum("amount"))["amount__sum"] or Decimal("0")
    )

    total_deduction = (
        Deduction.objects.filter(user=request.user)
        .aggregate(Sum("amount"))["amount__sum"] or Decimal("0")
    )
    
    context = calculate_tax_summary(total_income, total_deduction)
    
    create_notification(
        request.user,
        "Tax Report Downloaded",
        "Income Tax Report PDF downloaded successfully.",
        "success"
    )

    pdf = generate_tax_pdf(context)

    return FileResponse(
        pdf,
        as_attachment=True,
        filename="Income_Tax_Report.pdf"
    )