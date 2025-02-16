# from django.contrib import admin
# from notifications.models import Notification

# # Check if Notification is already registered before registering again
# if not admin.site.is_registered(Notification):
#     @admin.register(Notification)
#     class NotificationAdmin(admin.ModelAdmin):
#         list_display = ('recipient', 'verb', 'description', 'timestamp')
#         list_filter = ('verb', 'timestamp')
#         search_fields = ('description',)
