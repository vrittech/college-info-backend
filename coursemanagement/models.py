from django.db import models
from level.models import Level
from faculty.models import Faculty
from affiliation.models import Affiliation

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='course_level')
    faculties = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='course_faculties')
    affiliations = models.ManyToManyField('affiliation.Affiliation')
    duration = models.CharField(max_length=50)
    description = models.TextField()
    excerpt = models.TextField()
    image = models.ImageField(upload_to='courses/images/')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    
 