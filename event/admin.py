from django.contrib import admin
from .models import Event,EventOrganizer,EventCategory,EventGallery
# Register your models here.
admin.site.register(Event)
admin.site.register(EventOrganizer)
admin.site.register(EventCategory)
admin.site.register(EventGallery)