from django.db import models
from django.conf import settings
import os

class BucketFile(models.Model):
    """
    Simplified model to track files with minimal fields
    """
    file = models.FileField(upload_to='bucket_files/', null=True, blank=True)  # Actual file storage
    name = models.CharField(max_length=255, blank=True, null=True)  # ✅ New field for filename
    content_type = models.CharField(max_length=255, blank=True, null=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
    # Automatically populated fields
    size = models.BigIntegerField(blank=True, null=True)
    # url = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        verbose_name = "Bucket File"
        verbose_name_plural = "Bucket Files"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        """Auto-populate size, URL, and file name"""
        if self.file:
            self.size = self.file.size
            # self.url = self.get_absolute_url()
            self.name = os.path.basename(self.file.name)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.name or "No file"
