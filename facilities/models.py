from django.db import models
from collegemanagement.models import College
# class Category(models.Model):
#     name = models.CharField(max_length=255)
#     image = models.ImageField(upload_to='facility_images/', blank=True, null=True)
#     created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

#     def __str__(self):
#         return self.name

class Facility(models.Model):
    name = models.CharField(max_length=255)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='facilities')
    image = models.ImageField(upload_to='facility_images/', blank=True, null=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_show = models.BooleanField(default=False)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    

    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ('manage_facility', 'Manage facility'),
        ]

class CollegeFacility(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='college_facilities')
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='college_facilities')
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True) 
    
    def __str__(self):
        return f'{self.college.name} - {self.facility.name}'
    
    class Meta:
        permissions = [
            ('manage_collegefacility', 'Manage collegefacility'),
        ]