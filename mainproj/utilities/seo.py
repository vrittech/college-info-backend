from django.db import models

class SEOFields(models.Model):
    meta_title = models.CharField(max_length=255, blank=True, null=True, help_text="Title for search engines.")
    meta_tag = models.CharField(max_length=255, blank=True, null=True, help_text="Primary meta tag for SEO.")
    meta_description = models.TextField(blank=True, null=True, help_text="Short description for SEO.")
    meta_keywords = models.TextField(blank=True, null=True, help_text="Comma-separated keywords for SEO.")
    meta_author = models.CharField(max_length=255, blank=True, null=True, help_text="Author information for SEO.")
    canonical_url = models.URLField(blank=True, null=True, help_text="Canonical URL to avoid duplicate content.")

    # Open Graph (OG) Tags (Social Sharing)
    og_title = models.CharField(max_length=255, blank=True, null=True, help_text="Title for social sharing.")
    og_description = models.TextField(blank=True, null=True, help_text="Description for social sharing.")
    og_url = models.URLField(blank=True, null=True, help_text="URL to share on social platforms.")
    og_image = models.ImageField(upload_to='college/og_image/', null=True, blank=True)
    og_type = models.CharField(max_length=50, blank=True, null=True, help_text="Type of the OG content (e.g., website, article).")
    og_locale = models.CharField(max_length=10, blank=True, null=True, default="en_US", help_text="Locale for OG tags (e.g., en_US).")
    
    # Dublin Core Metadata
    dc_title = models.CharField(max_length=255, blank=True, null=True, help_text="Title for Dublin Core Metadata.")
    dc_description = models.TextField(blank=True, null=True, help_text="Description for Dublin Core Metadata.")
    dc_language = models.CharField(max_length=10, blank=True, null=True, default="en", help_text="Language code for Dublin Core Metadata (e.g., en, fr).")

    class Meta:
        abstract = True  # Ensures this model is abstract and not a separate database table
