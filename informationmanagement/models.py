from django.db import models
from affiliation.models import Affiliation
# from college.models import College
from coursemanagement.models import Course
from collegemanagement.models import College
from district.models import District
from faculty.models import Faculty
from level.models import Level, SubLevel
# from semester.models import Semester  
from collegetype.models import CollegeType
# from collegeleveltype.models import CollegeLevelType
from certification.models import Certification
from mainproj.utilities.seo import SEOFields
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import uuid
from urllib.parse import urljoin
from django.conf import settings

class InformationTagging(models.Model):
    name = models.CharField(max_length=100,null=True,blank = True)
    url = models.URLField(blank=True, null=True)
    is_show = models.BooleanField(default=False)
    image = models.ImageField(upload_to='information_tagging/',null=True,blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return self.name if self.name else "Unnamed"
    
    class Meta:
        permissions = [
            ('manage_information_tagging', 'Manage Information Tagging'),
        ]


class InformationCategory(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    is_show = models.BooleanField(default=False)
    image = models.ImageField(upload_to='information_category/',null=True,blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
       return self.name if self.name else "Unnamed"
    
    def save(self, *args, **kwargs):
        # If is_show is being set to True, check the current count of True entries
        if self.is_show:
            count = InformationCategory.objects.filter(is_show=True).exclude(pk=self.pk).count()
            if count >= 2:
                raise ValidationError("Only two categories can be shown at a time.")
        
        if not self.slug:
            self.slug = slugify(self.name)
        
        super().save(*args, **kwargs)
    
    class Meta:
        permissions = [
            ('manage_information_category', 'Manage Information Category'),
        ]
    
class Information(SEOFields):
    # template_name  = models.CharField(max_length=255,null=True,blank=True)
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    title = models.CharField(max_length=510,unique=True)
    publish_date = models.DateField(null=True, blank=True)
    active_period_start = models.DateField(null=True, blank=True)
    active_period_end = models.DateField(null=True, blank=True)
    
    level = models.ManyToManyField(Level, blank=True)
    sublevel = models.ManyToManyField(SubLevel, blank=True)
    course = models.ManyToManyField(Course, blank=True)
    affiliation = models.ManyToManyField(Affiliation)
  
    district = models.ManyToManyField(District, blank=True)
    college = models.ManyToManyField(College, blank=True)
    faculty = models.ManyToManyField(Faculty, blank=True)
    
    information_tagging = models.ManyToManyField(InformationTagging, blank=True)
    information_category = models.ManyToManyField(InformationCategory, blank=True)
    
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # image = models.ManyToManyField(InformationGallery, blank=True)
    # file = models.ManyToManyField(InformationFiles, blank=True)
    state = models.BooleanField(default=False)
    featured_image = models.CharField(max_length = 500 , null = True,blank = True)


    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.title if self.title else "Unnamed"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.title)}-{str(self.public_id)[1:5]}{str(self.public_id)[-1:-5]}'
        super().save(*args, **kwargs)
    
    class Meta:
        permissions = [
            ('manage_information', 'Manage Information'),
        ]

    def get_active_period(self):
        return f"{self.active_period_start} to {self.active_period_end}"


class InformationFiles(models.Model):
    information  = models.ForeignKey(Information, on_delete=models.CASCADE,related_name='information_files')
    file = models.FileField(upload_to='information_docs/',null=True,blank=True)
    
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
   
    class Meta:
        permissions = [
            ('manage_informationfiles', 'Manage Information Files'),
        ]
        
class InformationGallery(models.Model):
    information = models.ForeignKey(Information, on_delete=models.CASCADE,related_name='information_gallery')
    image = models.ImageField(upload_to='information_category/',null=True,blank=True)
    is_featured = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        permissions = [
            ('manage_informationgallery', 'Manage Information Gallery'),
        ]
    
    def save(self, *args, **kwargs):
        # Ensure that only one featured image exists for this information
        if self.is_featured:
            # Unfeature any other images linked to this information
            InformationGallery.objects.filter(information=self.information, is_featured=True).update(is_featured=False)

        # Save the current instance first
        super().save(*args, **kwargs)

        # Update the Information model's featured_image field if this is the featured image
        if self.is_featured and self.image:
            # Update the `featured_image` field of the related `Information` instance
            self.information.featured_image = self.image.url
            self.information.save(update_fields=['featured_image'])  # Save only the updated field