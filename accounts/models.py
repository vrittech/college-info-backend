import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.text import slugify
from collegemanagement.models import College
from socialmedia.models import SocialMedia


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    # full_name = models.CharField(max_length=250, null=True, blank=True)
    college = models.ForeignKey(College, null=True, on_delete=models.SET_NULL, related_name='user', blank=True)
    social_media = models.ManyToManyField(SocialMedia, blank=True)
    email = models.EmailField(max_length=250, unique=True)
    position = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=15, null=True, default='')
    is_active = models.BooleanField(default=True)
    remarks = models.CharField(max_length=200,null=True,default = '')
    is_verified = models.BooleanField(default=False)
    
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

    avatar = models.ImageField(upload_to='profile', null=True, blank=True)
    professional_image = models.ImageField(upload_to='profile', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Remove 'username' from required fields

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-set first_name and last_name from full_name
        if self.full_name:
            name_parts = self.full_name.split(" ", 1)
            self.first_name = name_parts[0]
            self.last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Auto-generate username from full_name (if empty)
        if not self.username:
            base_username = slugify(self.full_name)[:30] if self.full_name else f"user-{uuid.uuid4().hex[:8]}"
            unique_username = base_username

            # Ensure uniqueness
            counter = 1
            while CustomUser.objects.filter(username=unique_username).exists():
                unique_username = f"{base_username}-{counter}"
                counter += 1

            self.username = unique_username

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email  # Display email instead of username

    class Meta:
        permissions = [
            ('manage_user', 'Manage User'),
        ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() if self.first_name or self.last_name else self.username

    @full_name.setter
    def full_name(self, value):
        name_parts = value.split(" ", 1)
        self.first_name = name_parts[0]
        self.last_name = name_parts[1] if len(name_parts) > 1 else ""
