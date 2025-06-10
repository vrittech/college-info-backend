from django.contrib import admin

# Register your models here.
from .models import Result, File
admin.site.register(Result)
admin.site.register(File)
