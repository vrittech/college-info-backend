# from django.db import models

# # Create your models here.
# event_name
# date
# duration
# type --> physical,online,hybrid
# online seat limit
# offline seat limit
# is_seat_limit
# venue
# links
# registration links
# is_registration
# registration type--> paid,free 
# amount
# price type
#price_country
# description
# images foreign key from model(multiple images)
# is_featured image
#  organizer name foreign key from model
#  categories name foreign key from model
from django.db import models
from mainproj.utilities.seo import SEOFields
import uuid
from django.utils.text import slugify




class EventOrganizer(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_organizer/')
    link = models.URLField(blank=True, null=True)
    is_show = models.BooleanField(default=False)
    
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"

class Event(SEOFields):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    event_name = models.CharField(max_length=255,unique=True)
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    duration = models.CharField(max_length=255)
    TYPE_CHOICES = [
        ('physical', 'Physical'),
        ('online', 'Online'),
        ('hybrid', 'Hybrid'),
    ]
    event_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    venue = models.CharField(max_length=255, blank=True, null=True)
    
    online_seat_limit = models.PositiveIntegerField(default=0)
    offline_seat_limit = models.PositiveIntegerField(default=0)
    is_offline_seat_limit = models.BooleanField(default=False)
    is_online_seat_limit = models.BooleanField(default=False)
    
    is_registration = models.BooleanField(default=False)
    registration_link = models.URLField(blank=True, null=True)
    # event_links = models.URLField(blank=True, null=True)
    REGISTRATION_TYPE_CHOICES = [
        ('paid', 'Paid'),
        ('free', 'Free'),
    ]
    registration_type = models.CharField(max_length=10, choices=REGISTRATION_TYPE_CHOICES, default='free')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_type = models.CharField(max_length=100, blank=True, null=True)
    amount_country = models.CharField(max_length=100, blank=True, null=True)
    
    description = models.TextField(blank=True, null=True)
    is_featured_event = models.BooleanField(default=False)
    
    category = models.ManyToManyField(EventCategory, related_name='event_category')
    organizer = models.ManyToManyField(EventOrganizer, related_name='organizer')
    
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    
    def __str__(self):
        return f"{self.event_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.event_name)
        super().save(*args, **kwargs)
    
    
    class Meta:
        permissions = [
            ("manage_event", "Manage Event"),
        ]

class EventGallery(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='image')
    is_featured_image = models.BooleanField(default=False)
    image = models.ImageField(upload_to='event_images/',null=True,blank=True)
    
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.image.url} - {'Featured' if self.is_featured_image else 'Standard'}"
    
    class Meta:
        permissions = [
            ("manage_event_gallery", "Manage Event Gallery"),
        ]