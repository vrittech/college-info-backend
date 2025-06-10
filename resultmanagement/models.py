from django.db import models

class File(models.Model):
    file = models.FileField(
        upload_to="media/result/",
        null=True,
        blank=True,
        help_text="Upload your result file here",
        max_length=1000
    )
    name = models.CharField(max_length=512, null=True, blank=True)
    # Now store mapping JSON on File, not on Result:
    mapped_json = models.JSONField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name


class Result(models.Model):
    student_name = models.CharField(max_length=512, null=True, blank=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    symbol_no = models.CharField(max_length=100, null=True, blank=True)
    dateofbirth = models.CharField(max_length=100, null=True, blank=True)
    cgpa = models.CharField(max_length=100, null=True, blank=True)
    remarks = models.CharField(max_length=512, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        # unique_together = ('file', 'symbol_no')
        indexes = [
            models.Index(fields=['symbol_no']),  
        ]
        

    def __str__(self):
        return self.symbol_no
