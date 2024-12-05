from django.db import models
from affiliation.models import Affiliation
# from college.models import College
from coursemanagement.models import Course
# from collegemanagement.models import College
from district.models import District
from faculty.models import Faculty
from level.models import Level, SubLevel
# from semester.models import Semester  
from collegetype.models import CollegeType
# from collegeleveltype.models import CollegeLevelType
from certification.models import Certification


class InformationTagging(models.Model):
    name = models.CharField(max_length=100,null=True,blank = True)
    url = models.URLField(blank=True, null=True)
    is_show = models.BooleanField(default=False)
    image = models.ImageField(upload_to='information_tagging/',null=True,blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return self.name


class InformationCategory(models.Model):
    name = models.CharField(max_length=100)
    is_show = models.BooleanField(default=False)
    image = models.ImageField(upload_to='information_category/',null=True,blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return self.name
    
class InformationGallery(models.Model):
    image = models.ImageField(upload_to='information_category/',null=True,blank=True)
    is_featured = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)


    def __str__(self):
        return self.created_date
    
class InformationFiles(models.Model):
    file = models.FileField(upload_to='information_docs/',null=True,blank=True)
    
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.created_date


class Information(models.Model):
    # template_name  = models.CharField(max_length=255,null=True,blank=True)
    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField()
    active_period_start = models.DateField()
    active_period_end = models.DateField()
    
    level = models.ManyToManyField(Level, blank=True)
    sublevel = models.ManyToManyField(SubLevel, blank=True)
    course = models.ManyToManyField(Course, blank=True)
    affiliation = models.ManyToManyField(Affiliation)
    college_type = models.ForeignKey(CollegeType, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ManyToManyField(District, blank=True)
    # college = models.ManyToManyField('collegemanagement.College', blank=True)
    faculty = models.ManyToManyField(Faculty, blank=True)
    
    information_tagging = models.ManyToManyField(InformationTagging, blank=True)
    information_category = models.ManyToManyField(InformationCategory, blank=True)
    
    short_description = models.TextField()
    description = models.TextField()
    image = models.ManyToManyField(InformationGallery, blank=True)
    file = models.ManyToManyField(InformationFiles, blank=True)
    # is_view = models.BooleanField(default=False)
    
    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="Title for search engines.")
    meta_tag = models.CharField(max_length=255, blank=True, null=True, help_text="Primary meta tag for SEO.")
    meta_description = models.TextField(blank=True, null=True, help_text="Short description for SEO.")
    meta_keywords = models.TextField(blank=True, null=True, help_text="Comma-separated keywords for SEO.")
    meta_author = models.CharField(max_length=255, blank=True, null=True, help_text="Author information for SEO.")
    canonical_url = models.URLField(blank=True, null=True, help_text="Canonical URL to avoid duplicate content.")

    # Open Graph (OG) Tags (Social Sharing)
    og_title = models.CharField(max_length=255, blank=True, null=True, help_text="Title for social sharing.")
    og_description = models.TextField(blank=True, null=True, help_text="Description for social sharing.")
    og_url = models.URLField(blank=True, null=True, help_text="URL to share on social platforms.")
    og_image =  models.ImageField(upload_to='college/og_image/',null=True,blank=True)
    og_type = models.CharField(max_length=50, blank=True, null=True, help_text="Type of the OG content (e.g., website, article).")
    og_locale = models.CharField(max_length=10, blank=True, null=True, default="en_US", help_text="Locale for OG tags (e.g., en_US).")
    
    # Dublin Core Metadata
    dc_title = models.CharField(max_length=255, blank=True, null=True, help_text="Title for Dublin Core Metadata.")
    dc_description = models.TextField(blank=True, null=True, help_text="Description for Dublin Core Metadata.")
    dc_language = models.CharField(max_length=10, blank=True, null=True, default="en", help_text="Language code for Dublin Core Metadata (e.g., en, fr).")

    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_active_period(self):
        return f"{self.active_period_start} to {self.active_period_end}"
