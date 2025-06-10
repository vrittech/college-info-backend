from django.db import models

class PlacementPosition(models.Model):
    TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('result', 'Result')
    ]
    placement_name = models.CharField(max_length=255,null=True,blank=True) 
    duration_in_seconds = models.IntegerField(default=0)  # Time in seconds
    adv_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='normal'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.placement_name
    
    class Meta:
        permissions = [
            ('manage_placementposition', 'Manage Placement Position'),
        ]


class Advertisement(models.Model):
    TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('result', 'Result')
    ]
    name = models.CharField(max_length=255)
    link = models.URLField(null=True,blank=True)
    adv_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='normal'
    )
    is_show = models.BooleanField(default=False)
    image = models.ImageField(upload_to='ads/',null=True,blank=True)
    placement = models.ForeignKey(PlacementPosition, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    # duration_in_seconds = models.IntegerField(default=0)  # Time in seconds for the ad

    # def __str__(self):
    #     return self.name
    class Meta:
        permissions = [
            ('manage_advertisement', 'Manage Advertisement'),
        ]
    
 
