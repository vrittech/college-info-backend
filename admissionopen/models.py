from django.db import models

# Create your models here.
# AdmissionOpen Model
class AdmissionOpen(models.Model):
    admission_year = models.IntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'Admission {self.admission_year} - {"Open" if self.status else "Closed"}'