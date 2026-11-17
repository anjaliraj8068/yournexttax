from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from income.models import Income
from django.db.models import Sum,Count
from income.models import Income
from deductions.models import Deduction
from decimal import Decimal


def home(request):
    return render(request, "home.html", {"hide_sidebar": True})

@login_required
def dashboard(request):

    incomes = Income.objects.filter(user=request.user)

    deductions = Deduction.objects.filter(user=request.user)

    total_income = (
        incomes.aggregate(Sum("amount"))["amount__sum"] or 0
    )

    total_deduction = (
        deductions.aggregate(Sum("amount"))["amount__sum"] or 0
    )

    taxable_income = max(
        total_income - total_deduction,
        0
    )

    tax = taxable_income * Decimal("0.10")

    latest_incomes = incomes.order_by("-created_at")[:5]

    latest_deductions = deductions.order_by("-created_at")[:5]

    ai_score = 100

    if total_deduction < 150000:
        ai_score -= 15

    if tax > 50000:
        ai_score -= 10

    if total_income == 0:
        ai_score = 0

    context = {

        "total_income": total_income,
        "total_deduction": total_deduction,
        "taxable_income": taxable_income,
        "tax": tax,

        "income_count": incomes.count(),
        "deduction_count": deductions.count(),

        "latest_incomes": latest_incomes,
        "latest_deductions": latest_deductions,

        "ai_score": ai_score,

    }

    return render(
        request,
        "dashboard.html",
        context
    )

def about(request):
    return render(request, "about.html", {"hide_sidebar": True})

def support(request):
    return render(request, "support.html", {"hide_sidebar": True})
