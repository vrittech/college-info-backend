import sys
import traceback
import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Notification
from .serializers import NotificationSerializer

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
        """Return notifications based on user role with recursion handling."""
        try:
            if self.request.user.is_superuser:
                return Notification.objects.all().order_by("-timestamp")
            return Notification.objects.filter(user=self.request.user).order_by("-timestamp")
        except RecursionError:
            logger.error("RecursionError in get_queryset() - Too many recursive calls.", exc_info=True)
            sys.setrecursionlimit(5000)  # Increase recursion limit safely
            return Notification.objects.none()  # Return empty queryset to prevent API failure

    def update(self, request, *args, **kwargs):
        """Mark a single notification as read with recursion handling."""
        try:
            instance = self.get_object()
            if request.user != instance.user:
                return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

            instance.is_read = True
            instance.save()
            return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
        except RecursionError:
            logger.error("RecursionError in update() - Too many recursive calls.", exc_info=True)
            sys.setrecursionlimit(5000)
            return Response({"error": "Recursion limit exceeded"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Error in update(): {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while marking notification as read."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["POST"])
    def mark_all_as_read(self, request):
        """Mark all notifications as read for the requesting user with recursion handling."""
        try:
            notifications = Notification.objects.filter(user=request.user, is_read=False)
            count = notifications.update(is_read=True)
            return Response({"message": f"{count} notifications marked as read"}, status=status.HTTP_200_OK)
        except RecursionError:
            logger.error("RecursionError in mark_all_as_read() - Too many recursive calls.", exc_info=True)
            return Response({"error": "Recursion limit exceeded"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Error in mark_all_as_read(): {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while marking notifications as read."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=["DELETE"])
    def delete_all(self, request):
        """Delete all notifications for the requesting user with recursion handling."""
        try:
            if request.user.is_superuser:
                count, _ = Notification.objects.all().delete()
            else:
                count, _ = Notification.objects.filter(user=request.user).delete()
            return Response({"message": f"{count} notifications deleted"}, status=status.HTTP_200_OK)
        except RecursionError:
            logger.error("RecursionError in delete_all() - Too many recursive calls.", exc_info=True)
            return Response({"error": "Recursion limit exceeded"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Error in delete_all(): {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while deleting notifications."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
