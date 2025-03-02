from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    ROLE_CHOICES = [
    ('student', 'Student'),
    ('others', 'Others'),
    ('college_admin', 'College Admin'),
]
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    phone_number = models.CharField(max_length=15,null=True,blank=True)
    tag = models.CharField(
    max_length=20,
    choices=ROLE_CHOICES,
    default='others',
)
    subject = models.CharField(max_length=1000,null=True,blank=True)
    message = models.TextField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ('manage_contact', 'Manage contact'),
        ]