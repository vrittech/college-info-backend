from django.db import models
from level.models import Level
from faculty.models import Faculty
from affiliation.models import Affiliation
from discipline.models import Discipline
from duration.models import Duration
from mainproj.utilities.seo import SEOFields
import uuid
from django.utils.text import slugify

# Create your models here.
class Course(SEOFields):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255,unique=True)
    abbreviation = models.CharField(max_length=255)
    duration = models.ForeignKey(Duration,on_delete=models.CASCADE,related_name='course_duration')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='course_faculties')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='course_level')
    affiliation = models.ForeignKey(Affiliation, on_delete=models.CASCADE,related_name='course_affiliation',blank=True,null=True)
    discipline = models.ManyToManyField(Discipline, related_name='course_discipline')
    description = models.TextField(default = "")
    course_shortdescription = models.TextField(default = "")
    course_outcome = models.TextField(default = "")
    course_curriculum = models.TextField(default = "")
    eligibility_criteria = models.TextField(default = "")
    image = models.ImageField(upload_to='courses/images/',null=True,blank=True)
    # curriculum_file_upload = models.FileField(upload_to='courses/pdf/',null=True,blank=True
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Course"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        permissions = [
            ('manage_course', 'Manage course'),
        ]

    
class CourseCurriculumFile(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="curriculum_file_upload")
    curriculum_file_upload = models.FileField(upload_to="courses/curriculum_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.course.name} - {self.file.name}"
    class Meta:
        permissions = [
            ('manage_coursecurriculumfile', 'Manage manage_coursecurriculumfile'),
        ]