from django.db import models

# CoursesAndFees Model
class CoursesAndFees(models.Model):
    course_name = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.course_name} - {self.fee}'