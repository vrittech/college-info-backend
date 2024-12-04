from django.db import models

# Create your models here.
class Duration(models.Model):
    name = models.CharField(max_length=255)
    
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
