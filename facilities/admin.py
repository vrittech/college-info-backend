from django.contrib import admin

# Register your models here.
from .models import Facility,CollegeFacility
admin.site.register(Facility)
admin.site.register(CollegeFacility)
