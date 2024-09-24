from django.db import models

# Create your models here.
# Facilities Model
class Facility(models.Model):
    facility_name = models.CharField(max_length=255)

    def __str__(self):
        return self.facility_name