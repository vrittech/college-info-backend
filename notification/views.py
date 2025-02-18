# from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from notifications.models import Notification
# from .serializers import NotificationSerializer
# from notifications.signals import notify
# from accounts.models import CustomUser as User

# # User = get_user_model()

# # 📌 API to get all notifications for a user
# class NotificationListView(generics.ListAPIView):
#     serializer_class = NotificationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return self.request.user.notifications.all()  # Get notifications for the authenticated user


# # 📌 API to get only unread notifications
# class UnreadNotificationsView(generics.ListAPIView):
#     serializer_class = NotificationSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return self.request.user.notifications.unread()  # Filter only unread notifications


# # 📌 API to mark a notification as read
# class MarkNotificationAsReadView(generics.UpdateAPIView):
#     serializer_class = NotificationSerializer
#     permission_classes = [IsAuthenticated]

#     def patch(self, request, *args, **kwargs):
#         notification = Notification.objects.get(id=kwargs["pk"], recipient=request.user)
#         notification.mark_as_read()  # Mark notification as read
#         return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)


# # 📌 API to send a notification
# class SendNotificationView(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         recipient_id = request.data.get("recipient_id")
#         verb = request.data.get("verb")
#         description = request.data.get("description", "")

#         recipient = User.objects.get(id=recipient_id)
#         notify.send(request.user, recipient=recipient, verb=verb, description=description)

#         return Response({"message": "Notification sent"}, status=status.HTTP_201_CREATED)
