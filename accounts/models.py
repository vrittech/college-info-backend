from django.db import models
from django.contrib.auth.models import AbstractUser
# from department.models import Department

# Create your models here.
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='profile',null=True,blank=True)
    professional_image = models.ImageField(upload_to='profile',null=True,blank=True)

    full_name = models.CharField(max_length = 250)
    position = models.CharField(max_length = 250,null = True)
    # department = models.ForeignKey(Department,null = True,on_delete = models.SET_NULL)
    position = models.CharField(max_length = 250)
    email = models.EmailField(max_length = 250,unique = True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username
    
    class Meta:
        permissions = [
            ('can_verify_user', 'Can verify user'),
        ]


