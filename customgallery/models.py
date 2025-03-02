from django.db import models

# Create your models here.

class CustomGallery(models.Model):
    name = models.CharField(max_length = 500 , null = True,blank = True)
    image = models.FileField(max_length = 500,upload_to = 'gallery/images')
    created_date = models.DateField(auto_now_add=True, null = True,blank = True)
    created_date_time = models.DateTimeField(auto_now_add=True, null = True,blank = True)
    updated_date_time = models.DateTimeField(auto_now=True, null = True,blank = True)
    
    def __str__(self) -> str:
        return f"{str(self.name)}:{str(self.created_date)}"

