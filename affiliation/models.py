
#    name
#    established_year
#    address url
#    address
#    Location--->foreign/Domestic
#    phone_number
#    email
#    links
#    Course------> manytoMany
#    AffiliatedCollege-----> college model manytomany
#    Level 
#    salientFetaures
#    description
#    feature 
#    file upload


from django.db import models
from course.models import Course
from college.models import College
from level.models import Level
from location.models import Location

class Affiliation(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    established_year = models.IntegerField(default=2024)
    google_map_embed_url = models.URLField(max_length=500, blank=True, null=True)
    address = models.TextField(max_length=500,null=True,blank=True)
    location = models.ForeignKey(Location,on_delete=models.CASCADE, related_name='affiliation_location')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website_url = models.URLField(max_length=500, blank=True, null=True)
    courses = models.ManyToManyField(Course, related_name='affiliations_courses')
    affiliated_colleges = models.ManyToManyField(College, related_name='affiliations_college')
    level = models.ManyToManyField(Level, related_name='affiliations_level')
    salient_features = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    feature_image = models.ImageField(upload_to='affiliation_image/',null=True,blank=True)
    file_upload = models.FileField(upload_to='affiliation_files/', blank=True, null=True)
    
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name

    