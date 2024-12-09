from django.db import models

# Create your models here.
class RequestSubmission(models.Model):
    subject = models.CharField(max_length=255)
    message =models.TextField()
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.subject 