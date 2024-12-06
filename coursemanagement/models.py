from django.db import models
from level.models import Level
from faculty.models import Faculty
from affiliation.models import Affiliation
from discipline.models import Discipline
from duration.models import Duration
from mainproj.utilities.seo import SEOFields
# Create your models here.
class Course(SEOFields):
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)
    duration = models.ForeignKey(Duration,on_delete=models.CASCADE,related_name='course_duration')
    faculties = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='course_faculties')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='course_level')
    discipline = models.ManyToManyField(Discipline, related_name='course_discipline')
    description = models.TextField(default = "")
    course_shortdescription = models.TextField(default = "")
    course_outcome = models.TextField(default = "")
    course_curriculum = models.TextField(default = "")
    eligibility_criteria = models.TextField(default = "")
    image = models.ImageField(upload_to='courses/images/')
    curriculum_file_upload = models.FileField(upload_to='courses/pdf/')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    
 