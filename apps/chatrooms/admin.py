from django.contrib import admin
from .models import ChatRoom, ChatMessage

# Register your models here.

admin.site.register(
    [
        ChatRoom,
        ChatMessage,
    ]
)  # Register your models here, e.g., admin.site.register(ChatRoom)
