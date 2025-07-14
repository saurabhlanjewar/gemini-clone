from rest_framework import generics, permissions
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer
from .tasks import call_gemini_api_async
from django.http import Http404
from django.core.cache import cache
from rest_framework.response import Response
from datetime import date
from rest_framework.response import Response


class ChatRoomListCreateView(generics.ListCreateAPIView):
    """List and create chatrooms."""

    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatRoom.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        chatroom = serializer.save(user=self.request.user)
        # Invalidate the cache for this user's chatrooms
        user_id = self.request.user.id
        cache_key = f"user_{user_id}_chatrooms"
        cache.delete(cache_key)

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        cache_key = f"user_{user_id}_chatrooms"
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 10)
        return Response(serializer.data)


class ChatMessageListView(generics.ListAPIView):
    """List messages in a chatroom."""

    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chatroom_id = self.kwargs.get("pk")
        return ChatMessage.objects.filter(
            chatroom_id=chatroom_id, chatroom__user=self.request.user
        )


def can_user_prompt(user):
    """Check if the user can prompt based on their subscription status."""
    profile = user.userprofile
    if profile.subscription_status == "pro":
        return True
    today = date.today()
    if profile.last_prompt_date != today:
        profile.last_prompt_date = today
        profile.daily_prompt_count = 0
    if profile.daily_prompt_count < 5:
        profile.daily_prompt_count += 1
        profile.save()
        return True
    return False


class ChatMessageCreateView(generics.CreateAPIView):
    """Create a new message in a chatroom."""

    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        chatroom_id = self.kwargs.get("pk")
        chatroom = ChatRoom.objects.get(id=chatroom_id, user=self.request.user)
        if not chatroom:
            raise Http404(
                "Chatroom not found or you do not have permission to access it."
            )
        if not can_user_prompt(self.request.user):
            raise Http404("You have reached your daily prompt limit.")

        message = serializer.save(chatroom=chatroom, user=self.request.user)
        # Call the Gemini API asynchronously
        call_gemini_api_async.delay(message.id)
