from django.db import models
from coursemanagement.models import Course
from collegemanagement.models import College

# CoursesAndFees Model
class CoursesAndFees(models.Model): #CollegeHaveCourse
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses_and_fees')
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='college_courses_and_fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_admission = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.created_date} - {self.amount}'