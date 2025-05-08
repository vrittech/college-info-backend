from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import BucketFile
from ..serializers.bucketfile_serializers import BucketFileListSerializers, BucketFileRetrieveSerializers, BucketFileWriteSerializers
from ..utilities.importbase import *
from django.conf import settings
from django.utils import timezone
import boto3
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..permissions import ViewOnlyOrSuperuserDelete
from django.db import models

EXCLUDED_PATHS = [
    'backup/',
    '/backup/',
    'database/backup/',
    '/database/backup/',
    'backup/database/',
    '/backup/database/',
    'static/',
    
]

class bucketfileViewsets(viewsets.ModelViewSet):
    serializer_class = BucketFileListSerializers
    permission_classes = [ViewOnlyOrSuperuserDelete]
    pagination_class = MyPageNumberPagination

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    # ✅ Enable search, ordering, and filtering
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'file','content_type']  # 'key' replaced with 'file' or 'name'
    ordering_fields = ['name', 'size', 'created_at']  # updated 'key' → 'name', 'last_modified' → 'created_at'
    filterset_fields = {
        'id': ['exact'],
        'created_at': ['exact', 'gte', 'lte'],
        'size': ['gte', 'lte'],
        'content_type': ['exact'],
    }

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BucketFileWriteSerializers
        elif self.action == 'retrieve':
            return BucketFileRetrieveSerializers
        return BucketFileListSerializers

    def get_queryset(self):
        queryset = BucketFile.objects.all().order_by('-id')
        # excluded_conditions = [~models.Q(key__startswith=path.lstrip('/')) for path in EXCLUDED_PATHS]
        # if excluded_conditions:
        #     from functools import reduce
        #     from operator import and_
        #     queryset = queryset.filter(reduce(and_, excluded_conditions))
        return queryset

    # def perform_destroy(self, instance):
    #     """Delete file from R2 and then delete from DB"""
    #     try:
    #         s3_client = boto3.client(
    #             's3',
    #             endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    #             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    #             region_name=settings.AWS_S3_REGION_NAME
    #         )
    #         s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=instance.key)
    #     except Exception as e:
    #         pass  # Optionally log the error
    #     instance.delete()

    # def create(self, request, *args, **kwargs):
    #     """Handle file upload to R2 bucket and DB entry"""
    #     file_obj = request.FILES.get('file')
    #     if not file_obj:
    #         return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

    #     file_name = request.data.get('name', file_obj.name)

    #     # 🚫 Prevent upload to excluded paths
    #     if any(file_name.startswith(p) for p in EXCLUDED_PATHS):
    #         return Response({'error': 'Uploads to this path are restricted.'}, status=status.HTTP_403_FORBIDDEN)

    #     try:
    #         s3_client = boto3.client(
    #             's3',
    #             endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    #             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    #             region_name=settings.AWS_S3_REGION_NAME
    #         )
    #         s3_client.upload_fileobj(
    #             file_obj,
    #             settings.AWS_STORAGE_BUCKET_NAME,
    #             file_name,
    #             ExtraArgs={
    #                 'ContentType': file_obj.content_type,
    #                 'CacheControl': 'max-age=86400'
    #             }
    #         )

    #         file_url = (
    #             f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}"
    #             if getattr(settings, 'AWS_S3_CUSTOM_DOMAIN', None)
    #             else f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{file_name}"
    #         )

    #         # Optional: if you have a `url` field in your model
    #         defaults = {
    #             'size': file_obj.size,
    #             'last_modified': timezone.now(),
    #             'content_type': file_obj.content_type,
    #             'extension': file_name.split('.')[-1].lower() if '.' in file_name else '',
    #             # 'url': file_url,  # Uncomment this line if `url` is a DB field
    #             'is_deleted': False
    #         }

    #         bucket_file, _ = BucketFile.objects.update_or_create(
    #             key=file_name,
    #             defaults=defaults
    #         )

    #         serializer = self.get_serializer(bucket_file)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)