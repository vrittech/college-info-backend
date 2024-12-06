from django.db import models
from affiliation.models import Affiliation
# from admissionopen.models import AdmissionOpen
# from location.models import Location
from collegetype.models import CollegeType
# from coursesandfees.models import CoursesAndFees
from facilities.models import Facility
from socialmedia.models import SocialMedia
from district.models import District
from discipline.models import Discipline
from gallery.models import Gallery
# from accounts.models import CustomUser
from formprogress.models import FormStepProgress
from mainproj.utilities.seo import SEOFields
# from faqs.models import FAQs

 
# CollegeGallery Model
class CollegeGallery(models.Model):
    image = models.ImageField(upload_to='college/gallery/')
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'Gallery Image {self.id}'
    
class Placement(models.Model):
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'Placement {self.id}'


    
class College(SEOFields):
    banner_image = models.ImageField(upload_to='college/banner/')
    dp_image = models.ImageField(upload_to='college/dp/')
    name = models.CharField(max_length=255)
    established_date = models.DateField(null= True,blank=True)
    website_link = models.URLField(null= True,blank=True)
    address = models.CharField(max_length=255)
    district = models.ForeignKey(District,on_delete=models.CASCADE,related_name='college_district')
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    affiliated = models.ForeignKey(Affiliation, on_delete=models.CASCADE,related_name='college_affiliation')
    college_type = models.ForeignKey(CollegeType, on_delete=models.CASCADE,related_name='college_type')
    discipline = models.ManyToManyField(Discipline, related_name='college_discipline')
    social_media = models.ManyToManyField(SocialMedia)
    google_map_link = models.URLField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    about = models.TextField()
    brochure = models.FileField(upload_to='college/brochure/',null=True,blank=True)
    step_counter= models.ForeignKey(FormStepProgress, on_delete=models.CASCADE,related_name='step_counter')
    facilities = models.ManyToManyField(Facility,related_name='college_facilities')
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
        return self.name


class CollegeFaqs(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE,related_name='college_faq')
    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'Placement {self.id}'