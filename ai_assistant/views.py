from decimal import Decimal

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import FileResponse

from income.models import Income
from deductions.models import Deduction

from .models import AIReport
from .services import get_tax_recommendation
from .pdf_generator import generate_pdf
from notifications.services import create_notification


@login_required
def ai_recommendation_loading(request):
    """
    Renders an intermediate loading screen.
    The loading screen will automatically redirect to process_ai_recommendation.
    """
    return render(request, "ai_assistant/loading.html")


@login_required
def process_ai_recommendation(request):

    # --------------------------
    # Total Income
    # --------------------------

    total_income = (
        Income.objects.filter(user=request.user)
        .aggregate(Sum("amount"))["amount__sum"] or Decimal("0")
    )

    # --------------------------
    # Total Deduction
    # --------------------------

    total_deduction = (
        Deduction.objects.filter(user=request.user)
        .aggregate(Sum("amount"))["amount__sum"] or Decimal("0")
    )

    # --------------------------
    # Tax Calculation
    # --------------------------

    taxable_income = max(
        total_income - total_deduction,
        Decimal("0")
    )

    tax = taxable_income * Decimal("0.10")

    # --------------------------
    # Gemini AI Recommendation
    # --------------------------

    ai_response = get_tax_recommendation(
        total_income,
        total_deduction
    )

    # --------------------------
    # Format AI Response
    # --------------------------

    tips = []

    for line in ai_response.splitlines():

        line = line.strip()

        if not line:
            continue

        # Heading
        if line.startswith("##"):

            tips.append({
                "type": "heading",
                "text": line.replace("#", "").strip()
            })

            continue

        # Bullet Point
        if line.startswith(("*", "-", "•")):

            tips.append({
                "type": "tip",
                "text": line.lstrip("*-• ").strip()
            })

            continue

        # Normal Paragraph
        tips.append({
            "type": "text",
            "text": line
        })

    # --------------------------
    # Save AI Report
    # --------------------------

    report = AIReport.objects.create(
        user=request.user,
        total_income=total_income,
        total_deduction=total_deduction,
        tax_amount=tax,
        ai_response=ai_response,
    )
    create_notification(

        request.user,

        "AI Recommendation Ready",

        "Your AI Tax Recommendation has been generated successfully.",

        "info"
    )

    # --------------------------
    # Context
    # --------------------------

    context = {

        "report": report,

        "income": total_income,

        "deduction": total_deduction,

        "taxable_income": taxable_income,

        "tax": tax,

        "tips": tips,

        "ai_response": ai_response,

    }

    return render(
        request,
        "ai_assistant/ai_dashboard.html",
        context,
    )


# ==========================================================
# AI Report History
# ==========================================================

@login_required
def report_history(request):

    reports = AIReport.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "ai_assistant/history.html",
        {
            "reports": reports
        }
    )


# ==========================================================
# Download PDF
# ==========================================================

@login_required
def download_report(request, pk):

    report = AIReport.objects.get(
        id=pk,
        user=request.user
    )

    pdf = generate_pdf(report)

    return FileResponse(
        pdf,
        as_attachment=True,
        filename="Tax_Report.pdf"
    )


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from .services import get_chat_response


def chatbot(request):
    return render(request, "ai_assistant/chatbot.html")


@csrf_exempt
def chatbot_api(request):

    if request.method == "POST":

        data = json.loads(request.body)

        message = data.get("message")

        reply = get_chat_response(message)

        return JsonResponse({

            "reply": reply

        })