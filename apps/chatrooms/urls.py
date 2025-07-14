from django.urls import path
from .views import ChatRoomListCreateView, ChatMessageListView, ChatMessageCreateView


urlpatterns = [
    path("chatrooms", ChatRoomListCreateView.as_view(), name="chatroom-list-create"),
    path("chatroom/<int:pk>", ChatMessageListView.as_view(), name="chatroom-messages"),
    path(
        "chatroom/<int:pk>/message",
        ChatMessageCreateView.as_view(),
        name="chat-message-create",
    ),
]
