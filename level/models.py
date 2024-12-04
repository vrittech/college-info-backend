from django.db import models

# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='level/',null=True,blank=True)
    
    def __str__(self):
        
        return self.name
    
class SubLevel(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE,related_name='sublevel_level')
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='level/',null=True,blank=True)
    
    def __str__(self):
        
        return self.name