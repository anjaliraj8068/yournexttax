import re
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

styles = getSampleStyleSheet()

def generate_pdf(report):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    story = []

    # Modern Header
    story.append(Paragraph("<b><font size=18 color='#1d4ed8'>AI Tax Management Report</font></b>", styles["Title"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Generated For:</b> {report.user.username}", styles["Normal"]))
    story.append(Paragraph(f"<b>Date Generated:</b> {report.created_at.strftime('%d %b %Y %H:%M %p')}", styles["Normal"]))
    story.append(Spacer(1, 15))

    # Clean Table Layout for Financials
    table_data = [
        ["Financial Summary", "Amount (₹)"],
        ["Total Income", f"{report.total_income:,.2f}"],
        ["Total Deductions", f"{report.total_deduction:,.2f}"],
        ["Estimated Tax", f"{report.tax_amount:,.2f}"]
    ]

    financial_table = Table(table_data, colWidths=[250, 150])
    financial_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#3b82f6")),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0"))
    ]))
    
    story.append(financial_table)
    story.append(Spacer(1, 30))

    # AI Recommendation Header
    story.append(Paragraph("<b><font size=14 color='#0f172a'>Gemini AI Tax Recommendation</font></b>", styles["Heading2"]))
    story.append(Spacer(1, 15))

    # Basic Markdown Regex Parsing for ReportLab
    formated_html = ""
    for line in report.ai_response.splitlines():
        line = line.strip()
        if not line:
            formated_html += "<br/><br/>"
            continue
            
        # Parse Headers (###, ##, #)
        if line.startswith("### "):
            line = f"<b><font size=11 color='#1e293b'>{line[4:]}</font></b>"
        elif line.startswith("## "):
            line = f"<b><font size=12 color='#1e293b'>{line[3:]}</font></b>"
        elif line.startswith("# "):
            line = f"<b><font size=14 color='#1e293b'>{line[2:]}</font></b>"
            
        # Parse List items
        elif line.startswith("* ") or line.startswith("- "):
            line = f"&nbsp;&nbsp;&bull; {line[2:]}"
            
        # Parse Bold & Italics inline
        line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
        line = re.sub(r'\*(.*?)\*', r'<i>\1</i>', line)
        
        formated_html += line + "<br/>"

    # Custom style for AI response
    ai_style = styles["BodyText"]
    ai_style.leading = 16  # Improve line height

    story.append(Paragraph(formated_html, ai_style))

    doc.build(story)
    buffer.seek(0)
    return buffer