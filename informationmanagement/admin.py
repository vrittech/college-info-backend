from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Information, Year, Semester, InformationTagging, InformationCategory

admin.site.register(Year)
admin.site.register(InformationTagging)
admin.site.register(InformationCategory)

class InformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'course_level_type')
    search_fields = ('title', 'description')
    filter_horizontal = ('affiliation', 'course', 'level', 'district', 'college', 'faculty', 'years', 'semesters')

admin.site.register(Information, InformationAdmin)
