from django.db import models

# Create your models here.
class CollegeAndCourseInquiries(models.Model):
    full_name = models.CharField(max_length=510)  
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.first_name