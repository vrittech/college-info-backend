from django.apps import AppConfig


class BucketimagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bucketimages'
    
    def ready(self):
        # Import the signals module to ensure it's registered when the app is ready
        import bucketimages.signals
