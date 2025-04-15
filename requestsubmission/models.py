from django.db import models
from accounts.models import CustomUser

# Create your models here.
class RequestSubmission(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='request_submission', null=True, blank=True)
    subject = models.CharField(max_length=255)
    message =models.TextField()
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.subject 
    class Meta:
        permissions = [
            ("manage_requestsubmission", "Manage Request Submission"),
        ]