from django.db import models

# Create your models here.
class CollegeType(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='college_type/',null=True,blank=True)
    
    def __str__(self):
        return self.name