from celery import shared_task
from .models import ChatMessage
from .gemini import gemini_call


@shared_task
def call_gemini_api_async(message_id):
    """Asynchronously call the Gemini API for a chat message."""
    message = ChatMessage.objects.get(id=message_id)
    response = gemini_call(message.user_message)
    message.ai_response = response
    message.status = "completed"
    message.save()
