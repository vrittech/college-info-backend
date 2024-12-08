from django.contrib import admin

# Register your models here.
from .models import CollegeGallery,College,CollegeFaqs

admin.site.register(CollegeGallery)
admin.site.register(College)
admin.site.register(CollegeFaqs)