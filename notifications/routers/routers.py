from rest_framework.routers import DefaultRouter
from ..viewsets.notification_viewsets import notificationViewsets

router = DefaultRouter()


router.register('notification', notificationViewsets, basename="notificationViewsets")
