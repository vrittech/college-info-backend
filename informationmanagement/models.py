from django.db import models
from affiliation.models import Affiliation
from college.models import College
from course.models import Course
from district.models import District
from faculty.models import Faculty
from level.models import Level
from semester.models import Semester  # Assume this stores semester details
from collegetype.models import CollegeType


class Year(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class InformationTagging(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class InformationCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Information(models.Model):
    COURSE_LEVEL_TYPE_CHOICES = [
        ('Year', 'Year'),
        ('Semester', 'Semester')
    ]

    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField()
    active_period_start = models.DateField()
    active_period_end = models.DateField()
    course_level_type = models.CharField(
        max_length=10, 
        choices=COURSE_LEVEL_TYPE_CHOICES
    )
    affiliation = models.ManyToManyField(Affiliation, blank=True)
    course = models.ManyToManyField(Course, blank=True)
    level = models.ManyToManyField(Level, blank=True)
    college_type = models.ForeignKey(CollegeType, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ManyToManyField(District, blank=True)
    college = models.ManyToManyField(College, blank=True)
    faculty = models.ManyToManyField(Faculty, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='information_images/')
    information_tagging = models.ManyToManyField(InformationTagging, blank=True)
    information_category = models.ManyToManyField(InformationCategory, blank=True)

    # Dynamic relations for Year and Semester
    years = models.ManyToManyField(Year, blank=True)  
    semesters = models.ManyToManyField(Semester, blank=True)
    
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_active_period(self):
        return f"{self.active_period_start} to {self.active_period_end}"
