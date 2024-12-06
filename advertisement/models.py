from django.db import models

class PlacementPosition(models.Model):
    placement_name = models.CharField(max_length=255) 
    duration_in_seconds = models.IntegerField(default=0)  # Time in seconds
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position_name


class Advertisement(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    image = models.ImageField(upload_to='ads/')
    placement = models.ForeignKey(PlacementPosition, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # duration_in_seconds = models.IntegerField(default=0)  # Time in seconds for the ad

    def __str__(self):
        return self.name
