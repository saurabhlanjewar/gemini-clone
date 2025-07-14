import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)


def gemini_call(prompt):
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text
