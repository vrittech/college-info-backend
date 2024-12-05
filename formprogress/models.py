from django.db import models
# from accounts.models import CustomUser

# Create your models here.
class FormStepProgress(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # Optional for logged-in users
    form_name = models.CharField(max_length=255, default="college_information")  # Name of the form
    current_step = models.IntegerField(default=1)  # Step number the user is currently on
    completed = models.BooleanField(default=False)  # Whether the form was fully completed
    timestamp = models.DateTimeField(auto_now=True)  # Automatically updates on each interaction

    def __str__(self):
        status = "Completed" if self.completed else f"Step {self.current_step}"
        return f"{self.user or self.session_id} - {self.form_name} - {status}"
