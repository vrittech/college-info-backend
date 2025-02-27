from django.db import models
from affiliation.models import Affiliation
# from admissionopen.models import AdmissionOpen
# from location.models import Location
from collegetype.models import CollegeType
# from coursesandfees.models import CoursesAndFees
from facilities.models import Facility
from socialmedia.models import SocialMedia,CollegeSocialMedia
from district.models import District
from discipline.models import Discipline
from gallery.models import Gallery
# from accounts.models import CustomUser
from formprogress.models import FormStepProgress
from mainproj.utilities.seo import SEOFields
import uuid
from django.utils.text import slugify

 
# CollegeGallery Model

    
# class Placement(models.Model):
#     description = models.TextField(blank=True)
#     created_date = models.DateField(auto_now_add=True)
#     updated_date = models.DateField(auto_now=True)

#     def __str__(self):
#         return f'Placement {self.id}'
    
#     class Meta:
#         permissions = [
#             ('manage_placement', 'Manage placement'),
#         ]


    
class College(SEOFields):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    banner_image = models.ImageField(upload_to='college/banner/',null=True,blank=True)
    dp_image = models.ImageField(upload_to='college/dp/',null=True,blank=True)
    name = models.CharField(max_length=255)
    is_show = models.BooleanField(default=False)
    established_date = models.DateField(null= True,blank=True)
    website_link = models.URLField(null= True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE,related_name='college_district',null=True,blank=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(max_length=255,null=True,blank=True)
    affiliated = models.ForeignKey(Affiliation, on_delete=models.CASCADE,related_name='college_affiliation',null=True,blank=True)
    college_type = models.ForeignKey(CollegeType, on_delete=models.CASCADE,related_name='college_type',null=True,blank=True)
    discipline = models.ManyToManyField(Discipline, related_name='college_discipline',blank=True)
    # social_media = models.ManyToManyField(CollegeSocialMedia,blank=True)
    google_map_link = models.URLField(blank=True, null=True)
    latitude = models.CharField(max_length= 255,null=True,blank=True)
    longitude = models.CharField(max_length= 255,null=True,blank=True)
    about = models.TextField(null = True,blank=True)
    brochure = models.FileField(upload_to='college/brochure/',null=True,blank=True)
    step_counter= models.ForeignKey(FormStepProgress, on_delete=models.CASCADE,related_name='step_counter',null=True,blank=True)
    facilities = models.ManyToManyField(Facility,related_name='college_facilities',blank=True)
    placement = models.TextField(null=True,blank=True)
    scholarship = models.TextField(null=True,blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    # location = models.ForeignKey(Location,on_delete=models.CASCADE)
    # admission_open = models.ManyToManyField(AdmissionOpen)
    # college_gallery = models.ManyToManyField(CollegeGallery)
    # faqs = models.ManyToManyField(CollegeFaqs)
    # college_admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='college_admin')

    def map_location(self):
        
        return f'{self.latitude}, {self.longitude}'

    def __str__(self):
          return self.name if self.name else "Unnamed"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.name)}-{str(self.public_id)[1:5]}{str(self.public_id)[-1:-5]}'
        super().save(*args, **kwargs)
    
    
    class Meta:
        permissions = [
            ('manage_college', 'Manage college'),
        ]


class CollegeFaqs(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE,related_name='college_faq')
    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'Placement {self.id}'
    
    class Meta:
        permissions = [
            ('manage_faq', 'Manage faq'),
        ]

from django.db import models

class CollegeGallery(models.Model):
    college = models.ForeignKey(
        College, on_delete=models.CASCADE, related_name='college_gallery', null=True, blank=True
    )
    image = models.ImageField(upload_to='college/gallery/', null=True, blank=True)  # Store one image per instance
    # description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Gallery Image {self.id}'

    class Meta:
        permissions = [
            ('manage_college_gallery', 'Manage college gallery'),
        ]
