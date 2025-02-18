from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet
from django.urls import re_path
from .consumers import NotificationConsumer

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    path("", include(router.urls)),  # API for notifications
]

# WebSocket URL patterns
websocket_urlpatterns = [
    re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),  # WebSockets for real-time notifications
]
