from django.contrib import admin
from .models import Notification, NotificationUser

admin.site.register(Notification)
admin.site.register(NotificationUser)
