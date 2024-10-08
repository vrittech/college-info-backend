from django.db import models

# Create your models here.
class District(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    is_shown = models.BooleanField(default=False)
    # description = models.TextField(null=True,blank=True)
    # image = models.ImageField(upload_to='district/',null=True,blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.name