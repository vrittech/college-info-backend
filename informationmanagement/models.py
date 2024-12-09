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



class InformationTagging(models.Model):
    name = models.CharField(max_length=100,null=True,blank = True)
    url = models.URLField(blank=True, null=True)
    is_show = models.BooleanField(default=False)
    image = models.ImageField(upload_to='information_tagging/',null=True,blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ('manage_information_tagging', 'Manage Information Tagging'),
        ]


class InformationCategory(models.Model):
    name = models.CharField(max_length=100)
    is_show = models.BooleanField(default=False)
    image = models.ImageField(upload_to='information_category/',null=True,blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # If is_show is being set to True, check the current count of True entries
        if self.is_show:
            count = InformationCategory.objects.filter(is_show=True).exclude(pk=self.pk).count()
            if count >= 2:
                raise ValidationError("Only two categories can be shown at a time.")
        
        super().save(*args, **kwargs)
    
    class Meta:
        permissions = [
            ('manage_information_category', 'Manage Information Category'),
        ]
    

    



class Information(SEOFields):
    # template_name  = models.CharField(max_length=255,null=True,blank=True)
    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField()
    active_period_start = models.DateField()
    active_period_end = models.DateField()
    
    level = models.ManyToManyField(Level, blank=True)
    sublevel = models.ManyToManyField(SubLevel, blank=True)
    course = models.ManyToManyField(Course, blank=True)
    affiliation = models.ManyToManyField(Affiliation)
  
    district = models.ManyToManyField(District, blank=True)
    college = models.ManyToManyField(College, blank=True)
    faculty = models.ManyToManyField(Faculty, blank=True)
    
    information_tagging = models.ManyToManyField(InformationTagging, blank=True)
    information_category = models.ManyToManyField(InformationCategory, blank=True)
    
    short_description = models.TextField()
    description = models.TextField()
    # image = models.ManyToManyField(InformationGallery, blank=True)
    # file = models.ManyToManyField(InformationFiles, blank=True)
    state = models.BooleanField(default=False)

    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title
    
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
    def __str__(self):
        return self.created_date
    
    class Meta:
        permissions = [
            ('manage_information_files', 'Manage Information Files'),
        ]
        
class InformationGallery(models.Model):
    information = models.ForeignKey(Information, on_delete=models.CASCADE,related_name='information_gallery')
    image = models.ImageField(upload_to='information_category/',null=True,blank=True)
    is_featured = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.created_date
    
    class Meta:
        permissions = [
            ('manage_information_gallery', 'Manage Information Gallery'),
        ]