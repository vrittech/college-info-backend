from django.db import models
from collegemanagement.models import College

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
            ('manage_socialmedia', 'Manage Social Media'),
        ]
        
class CollegeSocialMedia(models.Model):
    name = models.ForeignKey(SocialMedia, on_delete=models.CASCADE,related_name='social_media',blank=True,null=True)
    # name= models.CharField(max_length=100,null= True,blank=True) 
    link = models.URLField(max_length=200)
    icon=models.ImageField(upload_to='components/banner',null = True,blank= True)
    is_show = models.BooleanField(default=False)
    updated_date = models.DateTimeField(auto_now=True, null = True,blank = True)
    college = models.ForeignKey(College, on_delete=models.CASCADE,related_name='college_social_media',null=True,blank=True)  
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.social_media.name
    permissions = [
        ('manage_collegesocialmedia', 'Manage college socialmedia'),
    ]