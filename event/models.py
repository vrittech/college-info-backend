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
from django.conf import settings
from urllib.parse import urljoin




class EventOrganizer(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_organizer/',null=True,blank=True)
    link = models.URLField(blank=True, null=True)
    is_show = models.BooleanField(default=False)
    
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"
    class Meta:
        permissions = [
            ("manage_eventorganizer", "Manage Event Organizer"),
        ]

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}"
    class Meta:
        permissions = [
            ("manage_eventcategory", "Manage Event Category"),
        ]

class Event(SEOFields):
    public_id = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    event_name = models.CharField(max_length=255)
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    duration = models.CharField(max_length=255)
    duration_type = models.CharField(max_length=255, blank=True, null=True)
    TYPE_CHOICES = [
        ('physical', 'Physical'),
        ('online', 'Online'),
        ('hybrid', 'Hybrid'),
    ]
    event_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    venue = models.CharField(max_length=255, blank=True, null=True)
    online_platform = models.CharField(max_length=255, blank=True, null=True)
    
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
    featured_image = models.CharField(max_length = 500 , null = True,blank = True)

    
    category = models.ManyToManyField(EventCategory, related_name='event_category')
    organizer = models.ManyToManyField(EventOrganizer, related_name='organizer')
    
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    

    
    def __str__(self):
        return f"{self.event_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.name)}-{str(self.public_id)[1:5]}{str(self.public_id)[-1:-5]}'
        super().save(*args, **kwargs)
    
    
    class Meta:
        permissions = [
            ("manage_event", "Manage Event"),
        ]

class EventGallery(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='image')
    is_featured_image = models.BooleanField(default=False)
    image = models.ImageField(upload_to='event_images/',null=True,blank=True)
    position = models.PositiveIntegerField(default=0)
    
    created_date_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        permissions = [
            ("manage_eventgallery", "Manage Event Gallery"),
        ]
    
    def save(self, *args, **kwargs):
        # Save the instance first to get a valid `image.url`
        super().save(*args, **kwargs)

        if self.is_featured_image and self.image:
            # Ensure SITE_URL is set in settings
            site_url = getattr(settings, "SITE_URL", "https://base.collegeinfonepal.com")  # Default fallback
            absolute_url = urljoin(site_url, self.image.url)  # Construct absolute URL

            # Save to event's featured_image field
            self.event.featured_image = absolute_url
            self.event.save(update_fields=['featured_image'])  # Update only the featured_image field