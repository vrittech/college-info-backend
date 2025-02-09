from django.db import models
from django.contrib.auth.models import AbstractUser
from collegemanagement.models import College
from django.contrib.auth.models import Group, Permission
from socialmedia.models import SocialMedia

# Create your models here.
class CustomUser(AbstractUser):
    # roles = models.CharField(max_length = 250,null = True) 
    full_name = models.CharField(max_length = 250,null = True)
    college = models.ForeignKey(College,null = True,on_delete = models.SET_NULL)
    social_media = models.ManyToManyField(SocialMedia,blank=True)
    email = models.EmailField(max_length = 250,unique = True)
    # social_links = models.ManyToManyField(SocialMedia,blank=True)
    position = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=15,null=True , default = '')
    
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Custom related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Custom related name
        blank=True
    )

    avatar = models.ImageField(upload_to='profile',null=True,blank=True)
    professional_image = models.ImageField(upload_to='profile',null=True,blank=True)

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
    
    @property
    def full_name(self):
        try:
            return self.first_name + " " + self.last_name
        except:
            return self.username


class GroupExtension(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='extension')
    position = models.PositiveIntegerField(default=0)
    
    def __int__(self):
        return self.position
    
    class Meta:
        permissions = [
            ('manage_group_extension', 'Manage group extension'),
        ]
    def save(self, *args, **kwargs):
        # Ensure the superuser status is not changed accidentally
        if not self.is_superuser:
            print("####################Superuser status cannot be changed.##################")
            # You can log or add checks here if needed
            pass
        super().save(*args, **kwar


    # def save(self, *args, **kwargs):
    #     # Set position to the Group ID if position is 0 (or could be None)
    #     if self.position == 0:
    #         super().save(*args, **kwargs)  # Save initially to get the group ID
    #         self.position = self.group.id
    #         super().save(*args, **kwargs)  # Save again to update position with group ID
    #     else:
    #         super().save(*args, **kwargs)
