from django.db import models

# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length = 500 , null = True,blank = True)
    featured_image = models.ImageField(max_length = 500,upload_to = 'gallery/feature_images')
    created_date = models.DateField(auto_now_add=True, null = True,blank = True)
    updated_date = models.DateTimeField(auto_now=True, null = True,blank = True)
    
    def __str__(self):
        return self.name

class Gallery(models.Model):
    image = models.ImageField(max_length = 500,upload_to = 'gallery/images')
    album = models.ManyToManyField(Album,related_name ="gallery")
    is_cover = models.BooleanField(default = False)
    
    created_date = models.DateField(auto_now_add=True, null = True,blank = True)
    created_date_time = models.DateTimeField(auto_now_add=True, null = True,blank = True)
    updated_date_time = models.DateTimeField(auto_now=True, null = True,blank = True)\
    
    def __str__(self):
        return self.created_date

