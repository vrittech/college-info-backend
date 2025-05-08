import os
from mimetypes import guess_type
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage
from bucketimages.models import BucketFile

# Import monitored models
from accounts.models import CustomUser
from collegemanagement.models import College, CollegeGallery
from advertisement.models import Advertisement
from affiliation.models import Affiliation
from certification.models import Certification
from coursemanagement.models import Course, CourseCurriculumFile
from event.models import EventGallery, Event, EventOrganizer
from facilities.models import Facility, CollegeFacility
from gallery.models import Gallery
from informationmanagement.models import (
    InformationGallery, Information, InformationFiles, InformationCategory
)
from level.models import Level, SubLevel
from popup.models import Popup
from socialmedia.models import SocialMedia, CollegeSocialMedia

# ✅ Model-to-file-fields mapping
MONITORED_MODELS = {
    CustomUser: ["professional_image", "avatar"],
    College: ["dp_image", "banner_image", "brochure"],
    CollegeGallery: ["image"],
    Advertisement: ["image"],
    Affiliation: ["logo_image", "cover_image"],
    Certification: ["image"],
    Course: ["image"],
    CourseCurriculumFile: ["curriculum_file_upload"],
    EventGallery: ["image"],
    EventOrganizer: ["image"],
    Facility: ["image"],
    CollegeFacility: ["image"],
    Gallery: ["image"],
    InformationGallery: ["image"],
    InformationFiles: ["file"],
    InformationCategory: ["image"],
    Level: ["image"],
    SubLevel: ["image"],
    Popup: ["image"],
    SocialMedia: ["icon"],
    CollegeSocialMedia: ["icon"],
}

def process_file_field(instance, field_name):
    """Handles saving file field data to BucketFile."""
    file_field = getattr(instance, field_name, None)
    if not file_field or not file_field.name:
        return

    if not file_field.storage.exists(file_field.name):
        return

    if not BucketFile.objects.filter(file=file_field.name).exists():
        BucketFile.objects.create(
            file=file_field,
            name=os.path.basename(file_field.name),
            content_type=guess_type(file_field.name)[0] or "application/octet-stream",
            object_id=instance.id,
        )

@receiver(post_save)
def sync_bucketfile_on_save(sender, instance, **kwargs):
    """Automatically store files in BucketFile after saving monitored models."""
    if sender not in MONITORED_MODELS:
        return

    for field in MONITORED_MODELS[sender]:
        try:
            process_file_field(instance, field)
        except Exception as e:
            print(f"⚠️ Error processing {sender.__name__}.{field} (ID: {instance.id}): {e}")
