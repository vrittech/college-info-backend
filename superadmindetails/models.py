from django.db import models

# Create your models here.
from django.db import models

class SuperAdminDetails(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15,null=True, blank=True)
    location = models.CharField(max_length=255,null=True, blank=True)
    messenger_link = models.CharField(max_length=510,null=True, blank=True)
    facebook_link = models.CharField(max_length=510,null=True, blank=True)
    x_link = models.CharField(max_length=510,null=True, blank=True)
    youtube_link = models.CharField(max_length=510,null=True, blank=True)
    linkedin_link = models.CharField(max_length=510,null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        permissions=[
            ('manage_superadmindetails', 'Manage Super Admin Details'),
        ]
