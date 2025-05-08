# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from ...models import BucketFile, BucketSyncLog
# from django.conf import settings
# import boto3
# import logging

# logger = logging.getLogger(__name__)

# EXCLUDED_PATHS = [
#     'backup/',
#     'database/backup/',
#     'backup/database/',
#     'static/',
#     'media/',
# ]

# class Command(BaseCommand):
#     help = 'Synchronizes the database with the R2 bucket contents'

#     def handle(self, *args, **options):
#         sync_log = BucketSyncLog.objects.create(started_at=timezone.now())

#         try:
#             # Setup S3 client
#             s3_client = boto3.client(
#                 's3',
#                 endpoint_url=settings.AWS_S3_ENDPOINT_URL,
#                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#                 region_name=settings.AWS_S3_REGION_NAME
#             )

#             paginator = s3_client.get_paginator('list_objects_v2')
#             page_iterator = paginator.paginate(Bucket=settings.AWS_STORAGE_BUCKET_NAME)

#             r2_keys = set()
#             unchanged_files = 0
#             skipped_files = 0

#             for page in page_iterator:
#                 for obj in page.get('Contents', []):
#                     key = obj['Key']

#                     # ✅ Skip excluded paths
#                     if any(key.startswith(path) for path in EXCLUDED_PATHS):
#                         skipped_files += 1
#                         continue

#                     r2_keys.add(key)

#                     defaults = {
#                         'size': obj['Size'],
#                         'last_modified': obj['LastModified'],
#                         'content_type': obj.get('ContentType'),
#                         'extension': key.split('.')[-1].lower() if '.' in key else '',
#                         'url': obj.get('WebsiteRedirectLocation'),
#                         'cache_control': obj.get('CacheControl'),
#                         'etag': obj.get('ETag'),
#                         'is_deleted': False,
#                     }

#                     bucket_file, created = BucketFile.objects.update_or_create(
#                         key=key,
#                         defaults=defaults
#                     )

#                     if created:
#                         sync_log.new_files += 1
#                     elif any(getattr(bucket_file, k) != v for k, v in defaults.items() if hasattr(bucket_file, k)):
#                         sync_log.updated_files += 1
#                     else:
#                         unchanged_files += 1

#             # ✅ Delete all entries from excluded paths in DB
#             excluded_deleted = 0
#             for path in EXCLUDED_PATHS:
#                 deleted_qs = BucketFile.objects.filter(key__startswith=path)
#                 count = deleted_qs.count()
#                 excluded_deleted += count
#                 deleted_qs.delete()

#             # Soft-delete remaining files not in R2
#             deleted_count = BucketFile.objects.exclude(key__in=r2_keys).update(is_deleted=True)
#             sync_log.deleted_files = deleted_count + excluded_deleted
#             sync_log.total_files = len(r2_keys)
#             sync_log.success = True
#             sync_log.completed_at = timezone.now()
#             sync_log.save()

#             self.stdout.write(self.style.SUCCESS(
#                 f"✅ Synced {sync_log.total_files} files | "
#                 f"🆕 New: {sync_log.new_files}, "
#                 f"🛠️ Updated: {sync_log.updated_files}, "
#                 f"🗑️ Deleted (R2-missing): {deleted_count}, "
#                 f"🚫 Skipped (excluded): {skipped_files}, "
#                 f"🧹 Cleaned (excluded from DB): {excluded_deleted}, "
#                 f"✅ Unchanged: {unchanged_files}"
#             ))

#         except Exception as e:
#             sync_log.error_message = str(e)
#             sync_log.completed_at = timezone.now()
#             sync_log.save()
#             logger.error(f"❌ Failed to sync R2 bucket: {str(e)}")
#             self.stderr.write(self.style.ERROR(f"❌ Sync failed: {str(e)}"))


import os
from mimetypes import guess_type
from django.core.management.base import BaseCommand
from django.utils import timezone
from bucketimages.models import BucketFile  
# Models
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
from socialmedia.models import SocialMedia,CollegeSocialMedia
from mimetypes import guess_type
from django.db.models import FileField, ImageField
from django.apps import apps
from bucketimages.models import BucketFile 

class Command(BaseCommand):
    help = "Extracts file fields from models and stores them in BucketFile table"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate the extraction without writing to the database',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        # ✅ Initialize counters
        processed_files = 0
        skipped_files = 0
        already_existing_files = 0

        model_config = [
            {"model": CustomUser, "fields": ["professional_image","avatar"]},
            {"model": College, "fields": ["dp_image", "banner_image","brochure"]},
            {"model": CollegeGallery, "fields": ["image"]},
            {"model": Advertisement, "fields": ["image"]},
            {"model": Affiliation, "fields": ["logo_image","cover_image"]},
            {"model": Certification, "fields": ["image"]},
            {"model": Course, "fields": ["image"]},
            {"model": CourseCurriculumFile, "fields": ["curriculum_file_upload"]},
            {"model": EventGallery, "fields": ["image"]},
            {"model": EventOrganizer, "fields": ["image"]},
            {"model": Facility, "fields": ["image"]},
            {"model": Gallery, "fields": ["image"]},
            {"model": InformationGallery, "fields": ["image"]},
            {"model": InformationFiles, "fields": ["file"]},
            {"model": InformationCategory, "fields": ["image"]},
            {"model": Level, "fields": ["image"]},
            {"model": SubLevel, "fields": ["image"]},
            {"model": Popup, "fields": ["image"]},
            {"model": SocialMedia, "fields": ["icon"]},
            {"model": CollegeSocialMedia, "fields": ["icon"]},
            
        ]

        self.stdout.write(self.style.SUCCESS("🚀 Starting file extraction process..."))

        for config in model_config:
            model = config["model"]
            field_names = config["fields"]
            model_key = f"{model._meta.app_label}.{model.__name__}"

            self.stdout.write(f"\n🔍 Processing model: {model_key}")

            for field_name in field_names:
                field_count = 0
                field_skipped = 0
                field_existing = 0

                for instance in model.objects.iterator():
                    try:
                        file_field = getattr(instance, field_name, None)
                        if not file_field or not file_field.name:
                            continue

                        if not file_field.storage.exists(file_field.name):
                            self.stdout.write(f"    ❌ File not found: {file_field.name}")
                            skipped_files += 1
                            field_skipped += 1
                            continue

                        if BucketFile.objects.filter(file=file_field.name).exists():
                            self.stdout.write(f"    ⏩ Already exists: {file_field.name}")
                            already_existing_files += 1
                            field_existing += 1
                            continue

                        if not dry_run:
                            content_type = guess_type(file_field.name)[0] or "application/octet-stream"
                            BucketFile.objects.create(
                                file=file_field,
                                name=os.path.basename(file_field.name),
                                content_type=content_type,
                                object_id=instance.id,
                            )


                        processed_files += 1
                        field_count += 1

                    except Exception as e:
                        self.stdout.write(self.style.WARNING(
                            f"    ⚠️ Error in {field_name} for {model_key} (ID {instance.id}): {e}"
                        ))
                        skipped_files += 1
                        field_skipped += 1

                self.stdout.write(
                    f"    ✅ {field_count} processed | "
                    f"⏩ {field_existing} already existed | "
                    f"🚫 {field_skipped} skipped for field '{field_name}'"
                )

        self.stdout.write(self.style.SUCCESS("\n🎉 Extraction summary:"))
        self.stdout.write(f"   🆕 New files added     : {processed_files}")
        self.stdout.write(f"   ⏩ Already existing    : {already_existing_files}")
        self.stdout.write(f"   🚫 Skipped (missing/failed): {skipped_files}")
        self.stdout.write(f"   Mode                  : {'DRY RUN' if dry_run else 'LIVE'}")