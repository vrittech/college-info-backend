from django.db import models
from django.conf import settings
from urllib.parse import urljoin


# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length = 500 , null = True,blank = True)
    featured_image = models.CharField(max_length = 500 , null = True,blank = True)
    created_date = models.DateField(auto_now_add=True, null = True,blank = True)
    updated_date = models.DateTimeField(auto_now=True, null = True,blank = True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        permissions = [
            ('manage_album', 'Manage Album'),
        ]

class Gallery(models.Model):
    image = models.ImageField(max_length = 500,upload_to = 'gallery/images',null=True,blank=True)
    album = models.ForeignKey(Album,related_name ="gallery",on_delete = models.CASCADE,null = True,blank = True)
    is_cover = models.BooleanField(default = False)
    
    created_date = models.DateField(auto_now_add=True, null = True,blank = True)
    created_date_time = models.DateTimeField(auto_now_add=True, null = True,blank = True)
    updated_date_time = models.DateTimeField(auto_now=True, null = True,blank = True)
    
    class Meta:
        permissions = [
            ('manage_gallery', 'Manage Gallery'),
        ]
        

    def save(self, *args, **kwargs):
        if self.is_cover and self.album:
            # Set all other images in this album to is_cover=False
            Gallery.objects.filter(album=self.album, is_cover=True).update(is_cover=False)

            # Update the album's featured image with the full absolute URL
            if self.image:
                # Save to album
                self.album.featured_image = self.image.url
                self.album.save(update_fields=['featured_image'])

        super().save(*args, **kwargs)

