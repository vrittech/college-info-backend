
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
# from coursemanagement.models import Course
from level.models import Level
# from location.models import Location
from district.models import District
# from collegetype.models import CollegeType
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from certification.models import Certification
from mainproj.utilities.seo import SEOFields
import uuid
from django.utils.text import slugify



def validate_year(value):
        current_year = now().year
        if value > current_year or value < 1800:  # Define a reasonable range
            raise ValidationError(f"{value} is not a valid year. Please provide a year between 1800 and {current_year}.")

class Affiliation(SEOFields):
    
    UNIVERSITY_TYPE_CHOICES = [
        ('local', 'Local'),
        ('foreign', 'Foreign'),
    ]
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255,null=True,blank=True,unique=True)
    established_year = models.IntegerField(default=now().year,validators=[validate_year])
    website_url = models.URLField(max_length=500, blank=True, null=True)
    google_map_embed_url = models.URLField(max_length=500, blank=True, null=True)
    latitude = models.CharField(max_length=100, null=True, blank=True) 
    longitude = models.CharField(max_length=100, null=True, blank=True) 
    address = models.CharField(max_length=500,null=True,blank=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE, related_name='affiliation_district')
    university_type = models.CharField(
        max_length=10,  # Set a maximum length appropriate for the choice values
        choices=UNIVERSITY_TYPE_CHOICES,
        default='local'
    )
    certification = models.ManyToManyField(Certification,related_name='affiliation_certification')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo_image = models.ImageField(upload_to='affiliation_image/',null=True,blank=True)
    cover_image = models.ImageField(upload_to='affiliation_image/',null=True,blank=True)
    
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
          return self.name if self.name else "Unnamed Affiliation"
    
    class Meta:
        permissions = [
            ('manage_affiliation', 'Manage Affiliation'),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    