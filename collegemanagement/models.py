from django.db import models
from affiliation.models import Affiliation
from admissionopen.models import AdmissionOpen
from location.models import Location
from collegetype.models import CollegeType
from coursesandfees.models import CoursesAndFees
from facilities.models import Facility
from socialmedia.models import SocialMedia

 
# CollegeGallery Model
class CollegeGallery(models.Model):
    image = models.ImageField(upload_to='college/gallery/')
    description = models.TextField(blank=True)

    def __str__(self):
        return f'Gallery Image {self.id}'

class College(models.Model):
    banner_image = models.ImageField(upload_to='college/banner/')
    dp_image = models.ImageField(upload_to='college/dp/')
    name = models.CharField(max_length=255)
    established_date = models.DateField()
    website_link = models.URLField()
    address = models.CharField(max_length=255)
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    affiliated = models.ForeignKey(Affiliation, on_delete=models.CASCADE)
    college_type = models.ForeignKey(CollegeType, on_delete=models.CASCADE)
    google_map_link = models.URLField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    about = models.TextField()
    courses_and_fees = models.ManyToManyField(CoursesAndFees)
    admission_open = models.ManyToManyField(AdmissionOpen)
    facilities = models.ManyToManyField(Facility)
    college_gallery = models.ManyToManyField(CollegeGallery)
    featured_video = models.FileField(upload_to='college/featured_videos/', blank=True, null=True)
    brochure = models.FileField(upload_to='college/brochure/')
    social_media = models.ManyToManyField(SocialMedia)
    scholarships = models.TextField()

    def map_location(self):
        return f'{self.latitude}, {self.longitude}'

    def __str__(self):
        return self.name
