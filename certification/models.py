from django.db import models

# Create your models here.
class Certification(models.Model):
    name = models.CharField(max_length=20, unique=True)
    is_show = models.BooleanField(default=False)
    image= models.ImageField(upload_to='certification/',null=True,blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name