from django.db import models
class Popup(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(null=True,blank=True)
    image = models.ImageField(upload_to='popups/',null=True,blank=True)
    duration_in_seconds = models.IntegerField(default=0)
    is_skipable = models.BooleanField(default=False)
    is_show = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    class Meta:
        permissions = [
            ('manage_popup', 'Manage Popup'),
        ]
    
 
