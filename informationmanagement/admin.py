from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Information, InformationTagging, InformationCategory

admin.site.register(InformationTagging)
admin.site.register(Information)
admin.site.register(InformationCategory)

