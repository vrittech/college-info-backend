from django.contrib import admin
from .models import Method,ModelMethod,MyModels
# Register your models here.
admin.site.register([Method,ModelMethod,MyModels])

