from django.db import models

# Create your models here.

class Gallery(models.Model):
    name = models.CharField(max_length = 500 , null = True,blank = True)
    image = models.ImageField(max_length = 500,upload_to = 'gallery/images')
    created_date = models.DateField(auto_now_add=True, null = True,blank = True)
    created_date_time = models.DateTimeField(auto_now_add=True, null = True,blank = True)
    updated_date_time = models.DateTimeField(auto_now=True, null = True,blank = True)

