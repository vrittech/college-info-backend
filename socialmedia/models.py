from django.db import models

# Create your models here.
class SocialMedia(models.Model):
    name= models.CharField(max_length=100,null= True,blank=True) 
    link = models.URLField(max_length=200)
    icon=models.ImageField(upload_to='components/banner',null = True,blank= True)
    is_show = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, null = True,blank = True)
    updated_date = models.DateTimeField(auto_now=True, null = True,blank = True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ('manage_social_media', 'Manage Social Media'),
        ]