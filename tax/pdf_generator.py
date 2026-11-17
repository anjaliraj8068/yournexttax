from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()


def generate_tax_pdf(context):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    story = []

    story.append(
        Paragraph(
            "<b>Income Tax Calculation Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    data = [

        ["Particular", "Amount (₹)"],

        ["Total Income", str(context["income"])],

        ["Total Deduction", str(context["deduction"])],

        ["Taxable Income", str(context["taxable_income"])],

        ["Old Regime Tax", str(context["old_tax"])],

        ["New Regime Tax", str(context["new_tax"])],

        ["Recommended Regime", context["better_regime"]],

        ["Tax Saving", str(context["tax_saving"])]

    ]

    table = Table(data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        ])

    )

    story.append(table)

    story.append(Spacer(1, 20))

    story.append(

        Paragraph(

            "<b>AI Suggestion</b>",

            styles["Heading2"]

        )

    )

    story.append(

        Paragraph(

            f"Recommended Regime : <b>{context['better_regime']}</b>",

            styles["BodyText"]

        )

    )

    story.append(Spacer(1, 10))

    story.append(

        Paragraph(

            f"<b>AI Recommendation:</b> {context['ai_recommendation']}",

            styles["BodyText"]

        )

    )

    doc.build(story)

    buffer.seek(0)

    return buffer