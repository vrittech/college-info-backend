from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    API for managing notifications.
    - Users only see their own notifications.
    - Superusers can see all notifications.
    - Users can mark notifications as read.
    - Users can delete their own notifications.
    - Superusers can delete all notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return notifications based on user role."""
        if self.request.user.is_superuser:
            return Notification.objects.all().order_by("-timestamp")
        return Notification.objects.filter(user=self.request.user).order_by("-timestamp")

    def update(self, request, *args, **kwargs):
        """Mark a single notification as read."""
        instance = self.get_object()
        if request.user != instance.user:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        instance.is_read = True
        instance.save()
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def mark_all_as_read(self, request):
        """Mark all notifications as read for the requesting user."""
        notifications = Notification.objects.filter(user=request.user, is_read=False)
        notifications.update(is_read=True)
        return Response({"message": "All notifications marked as read"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["DELETE"])
    def delete_all(self, request):
        """Delete all notifications for the requesting user."""
        if request.user.is_superuser:
            Notification.objects.all().delete()
        else:
            Notification.objects.filter(user=request.user).delete()
        return Response({"message": "All notifications deleted"}, status=status.HTTP_200_OK)
