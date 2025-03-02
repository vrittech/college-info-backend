from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Notification
from .serializers import NotificationSerializer
import logging

# Set up logging for debugging errors
logger = logging.getLogger(__name__)

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

    @action(detail=False, methods=['post'], name="Mark All as Read", url_path="mark_all_as_read")
    def mark_all_as_read(self, request, *args, **kwargs):
        """Mark all notifications as read for the requesting user."""
        try:
            print("🔍 mark_all_as_read action triggered")  # Debugging
            print(f"🔍 Current user: {request.user}")  # Debugging

            # Get all notifications for the current user that haven't been read by them
            notifications = Notification.objects.filter(user=request.user).exclude(read_by=request.user)
            print(f"🔍 Notifications to mark as read: {notifications.count()}")  # Debugging

            # Add the current user to the read_by field of each notification
            for notification in notifications:
                notification.read_by.add(request.user)
                print(f"🔍 Marked notification {notification.id} as read for user {request.user}")  # Debugging

            count = notifications.count()
            return Response({"message": f"{count} notifications marked as read"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in mark_all_as_read(): {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while marking notifications as read."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['delete'], name="Delete All Notifications", url_path="delete_all")
    def delete_all(self, request, *args, **kwargs):
        """Delete all notifications for the requesting user."""
        try:
            if request.user.is_superuser:
                count, _ = Notification.objects.all().delete()
            else:
                count, _ = Notification.objects.filter(user=request.user).delete()
            return Response({"message": f"{count} notifications deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in delete_all(): {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while deleting notifications."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], name="Mark as Read", url_path="mark_as_read")
    def mark_as_read(self, request, pk=None, *args, **kwargs):
        """Mark a single notification as read for the requesting user."""
        try:
            print("🔍 mark_as_read action triggered")  # Debugging
            notification = self.get_object()
            print(f"🔍 Notification ID: {notification.id}")  # Debugging

            if request.user != notification.user:
                return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

            # Add the current user to the read_by field
            notification.read_by.add(request.user)
            print(f"🔍 Marked notification {notification.id} as read for user {request.user}")  # Debugging

            serializer = self.get_serializer(notification, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in mark_as_read(): {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while marking the notification as read."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)