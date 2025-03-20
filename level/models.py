from django.db import models

# Create your models here.

    
class SubLevel(models.Model):
    
    name = models.CharField(max_length=255,null=True,blank=True)
    # description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='level/',null=True,blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    
    def __str__(self):
        return self.name if self.name else "Unnamed Sub Level"
    
    class Meta:
        permissions = [
            ('manage_sublevel', 'Manage SubLevel'),
        ]
    
class Level(models.Model):
    sublevel = models.ManyToManyField(SubLevel,related_name='sublevel_level',blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='level/',null=True,blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):        
        return self.name if self.name else "Unnamed Level"
    
    class Meta:
        permissions = [
            ('manage_level', 'Manage Level'),
        ]