from django.db import models

# Create your models here.
class SocialMedia(models.Model):
    icon=models.ImageField(upload_to='components/banner',null = True,blank= True)
    name= models.CharField(max_length=100,null= True,blank=True) 
    url = models.URLField(max_length=200)
    is_show = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, null = True,blank = True)
    updated_date = models.DateTimeField(auto_now=True, null = True,blank = True)
    
    def __str__(self):
        return self.name