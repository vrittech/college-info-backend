from django.db import models
from collegemanagement.models import College
from coursemanagement.models import Course

# full_name
# email
# phone 
# courses
# colleges
# message
from django.db import models
from collegemanagement.models import College
from coursemanagement.models import Course

class Inquiry(models.Model):
    # Personal Information
    full_name = models.CharField(max_length=255, help_text="Full name of the inquirer.")
    email = models.EmailField(help_text="Email address of the inquirer.")
    phone = models.CharField(max_length=15, help_text="Phone number of the inquirer.")

    # Relationships to College and Course
    courses = models.ManyToManyField(Course, related_name="inquiries", help_text="Courses the user is interested in.")
    colleges = models.ManyToManyField(College, related_name="inquiries", help_text="Colleges the user is interested in.")

    # Additional Message
    message = models.TextField(blank=True, null=True, help_text="Message or query from the user.")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="The time when the inquiry was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The last time the inquiry was updated.")

    def __str__(self):
        return f"Inquiry from {self.full_name} - {self.email}"
    
    class Meta:
        permissions = [
            ('manage_inquiry', 'Manage Inquiry'),
        ]
