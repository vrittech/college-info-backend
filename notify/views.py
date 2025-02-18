from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    API for managing notifications.
    - Users only see their own notifications.
    - Superusers can see all notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Notification.objects.all().order_by("-timestamp")
        return Notification.objects.filter(user=self.request.user).order_by("-timestamp")

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.user:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        instance.is_read = True
        instance.save()
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
