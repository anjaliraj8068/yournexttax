import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
from django.conf import settings

genai.configure(
    api_key=settings.GEMINI_API_KEY
)

model = genai.GenerativeModel("gemini-2.5-flash")


def get_tax_recommendation(income, deduction):

    prompt = f"""
You are an Indian Income Tax Expert.

User Details:

Total Income : ₹{income}

Total Deduction : ₹{deduction}

Give professional tax saving advice.

Rules:

1. Mention Section 80C.
2. Mention Section 80D.
3. Mention NPS.
4. Mention possible tax saving.
5. Answer in bullet points.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except ResourceExhausted:

        return """
⚠ Gemini API quota exceeded.

Please wait for about a minute and try again.

Meanwhile, you can continue using other features of the application.
"""

    except Exception as e:

        return f"AI Error: {str(e)}"


def get_chat_response(question):

    prompt = f"""

You are an Indian Income Tax AI Assistant.

Answer professionally.

Question:

{question}

Rules:

Use bullet points.

Keep answer under 100 words.

Mention Indian Income Tax Act whenever applicable.

"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception:

        return "Sorry, AI service is unavailable."