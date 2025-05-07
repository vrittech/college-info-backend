import boto3
from botocore.exceptions import ClientError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from urllib.parse import urlencode
from django.core.cache import cache
import logging
import math
import time
from .permissions import ViewOnlyOrSuperuserDelete
from rest_framework import filters
from .filter import BucketFileFilter
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime
from django.core.cache import cache

logger = logging.getLogger(__name__)

class BucketAPIView(APIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BucketFileFilter
    search_fields = ['name']  # Fields to search in
    ordering_fields = ['name', 'size', 'last_modified']  # Fields that can be ordered
    ordering = ['-last_modified']  # Default ordering
    permission_classes = [ViewOnlyOrSuperuserDelete]
    # Cache timeout in seconds (5 minutes)
    CACHE_TIMEOUT = 300
    # Default page size
    DEFAULT_PAGE_SIZE = 50
    # Maximum page size allowed
    MAX_PAGE_SIZE = 1000

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the client when the view is created
        self._s3_client = None
        
    def get_queryset(self):
        # Build cache key based on all filter parameters
        cache_key = f"bucket_files_{self.request.query_params.urlencode()}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data

        # Get filter parameters
        name_filter = self.request.query_params.get('name', '')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        # Convert dates to datetime objects once
        start_date_dt = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date_dt = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
        
        s3_client = self._get_r2_client()
        files = []
        list_params = {
            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'Prefix': name_filter.lower() if name_filter else '',  # Case-insensitive search
            'MaxKeys': 1000  # Limit number of results per request
        }
        
        # Paginate through results for large buckets
        while True:
            response = s3_client.list_objects_v2(**list_params)
            
            # Process and filter objects
            for obj in response.get('Contents', []):
                last_modified = obj['LastModified']
                
                # Apply date filters
                date_ok = True
                if start_date_dt and last_modified < start_date_dt:
                    date_ok = False
                if end_date_dt and last_modified > end_date_dt:
                    date_ok = False
                    
                if date_ok:
                    files.append({
                        'Key': obj['Key'],
                        'Size': obj['Size'],
                        'LastModified': last_modified
                    })
            
            # Check if there are more results
            if not response.get('IsTruncated'):
                break
                
            list_params['ContinuationToken'] = response['NextContinuationToken']
        
        # Cache the filtered results
        cache.set(cache_key, files, timeout=300)  # Cache for 5 minutes
        
        return files

    def _get_r2_client(self):
        """Initialize and return an R2 client"""
        if not all([
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY,
            settings.AWS_S3_ENDPOINT_URL
        ]):
            raise ValueError("R2 configuration is incomplete")
            
        if self._s3_client is None:
            self._s3_client = boto3.client(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
                config=boto3.session.Config(
                    connect_timeout=5,  # 5 seconds connection timeout
                    read_timeout=30,    # 30 seconds read timeout
                    retries={'max_attempts': 2}  # Only retry once
                )
            )
        return self._s3_client

    def _validate_config(self):
        """Validate that all required R2 config is present"""
        required_config = [
            'AWS_ACCESS_KEY_ID',
            'AWS_SECRET_ACCESS_KEY',
            'AWS_STORAGE_BUCKET_NAME',
            'AWS_S3_ENDPOINT_URL'
        ]
        missing_config = [key for key in required_config if not getattr(settings, key, None)]
        if missing_config:
            raise ValueError(f"Missing R2 configuration: {', '.join(missing_config)}")
    
    def _invalidate_cache(self):
        """
        Invalidate all cached file listings and individual file caches
        """
        # Delete all cached file listings
        keys = cache.keys('bucket_files_*') or []
        keys.extend(cache.keys('bucket_contents_*') or [])
        
        # Delete all cached file metadata
        file_keys = cache.keys('file_head_*') or []
        keys.extend(file_keys)
        
        # Delete all cached URLs
        url_keys = cache.keys('file_url_*') or []
        keys.extend(url_keys)
        
        if keys:
            cache.delete_many(keys)

    def _get_file_url(self, file_name):
        """Generate file URL with caching"""
        cache_key = f"file_url_{file_name}"
        url = cache.get(cache_key)
        if not url:
            if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN') and settings.AWS_S3_CUSTOM_DOMAIN:
                url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}"
            else:
                url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{file_name}"
            cache.set(cache_key, url, timeout=self.CACHE_TIMEOUT)
        return url

    def _build_pagination_url(self, request, page=None, size=None, limit=None, offset=None):
        """Build URL with updated pagination parameters"""
        params = request.query_params.copy()
        
        if page is not None:
            params['page'] = page
        if size is not None:
            params['size'] = size
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
            
        # Remove any None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return f"{request.build_absolute_uri(request.path)}?{urlencode(params)}"

    def _get_pagination_params(self, request):
        """Extract and validate pagination parameters"""
        # Default values
        page = 1
        size = self.DEFAULT_PAGE_SIZE
        limit = self.DEFAULT_PAGE_SIZE
        offset = 0
        using_page_size = False
        
        # Check which pagination method is being used
        if 'page' in request.query_params or 'size' in request.query_params:
            using_page_size = True
            try:
                page = int(request.query_params.get('page', 1))
                size = int(request.query_params.get('size', self.DEFAULT_PAGE_SIZE))
            except ValueError:
                raise ValueError("page and size must be integers")
            
            if page < 1 or size < 1:
                raise ValueError("page and size must be positive integers")
            if size > self.MAX_PAGE_SIZE:
                raise ValueError(f"Maximum page size is {self.MAX_PAGE_SIZE}")
                
            offset = (page - 1) * size
            limit = size
        elif 'limit' in request.query_params or 'offset' in request.query_params:
            try:
                limit = int(request.query_params.get('limit', self.DEFAULT_PAGE_SIZE))
                offset = int(request.query_params.get('offset', 0))
            except ValueError:
                raise ValueError("limit and offset must be integers")
            
            if limit < 0 or offset < 0:
                raise ValueError("limit and offset must be non-negative integers")
            if limit > self.MAX_PAGE_SIZE:
                raise ValueError(f"Maximum limit is {self.MAX_PAGE_SIZE}")
            
            size = limit
            page = (offset // size) + 1 if size > 0 else 1
        
        return {
            'page': page,
            'size': size,
            'limit': limit,
            'offset': offset,
            'using_page_size': using_page_size
        }

    def _get_cached_file_list(self):
        """Get cached file list or fetch fresh if not available"""
        cache_key = f"bucket_contents_{settings.AWS_STORAGE_BUCKET_NAME}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data['files'], cached_data['last_updated']
        
        # Not in cache, fetch from R2
        start_time = time.time()
        s3_client = self._get_r2_client()
        response = s3_client.list_objects_v2(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        files = response.get('Contents', [])
        
        # Prepare data for caching (ensure it's serializable)
        cacheable_files = []
        for file in files:
            cacheable_files.append({
                'Key': file['Key'],
                'Size': file['Size'],
                'LastModified': file['LastModified'].isoformat()
            })
        
        # Cache the result
        cache.set(cache_key, {
            'files': cacheable_files,
            'last_updated': time.time()
        }, timeout=self.CACHE_TIMEOUT)
        
        logger.info(f"Fetched {len(files)} files from R2 in {time.time() - start_time:.2f}s")
        return files, time.time()
    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    'file_name',
                    openapi.IN_QUERY,
                    description="Name of a specific file to retrieve",
                    type=openapi.TYPE_STRING
                ),
                openapi.Parameter(
                    'page',
                    openapi.IN_QUERY,
                    description="Page number (use with size)",
                    type=openapi.TYPE_INTEGER,
                    default=1
                ),
                openapi.Parameter(
                    'size',
                    openapi.IN_QUERY,
                    description="Number of items per page (use with page)",
                    type=openapi.TYPE_INTEGER,
                    default=50
                ),
                openapi.Parameter(
                    'limit',
                    openapi.IN_QUERY,
                    description="Maximum number of items to return (use with offset)",
                    type=openapi.TYPE_INTEGER,
                    default=50
                ),
                openapi.Parameter(
                    'offset',
                    openapi.IN_QUERY,
                    description="Starting position (use with limit)",
                    type=openapi.TYPE_INTEGER,
                    default=0
                )
            ],
            responses={
                200: openapi.Response(
                    description="List of files or single file details",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'files': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                                        'size': openapi.Schema(type=openapi.TYPE_INTEGER),
                                        'last_modified': openapi.Schema(type=openapi.TYPE_STRING),
                                        'url': openapi.Schema(type=openapi.TYPE_STRING)
                                    }
                                )
                            ),
                            'pagination': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'total_items': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'total_pages': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'current_page': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'page_size': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'limit': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'offset': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'has_next': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'has_previous': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'next_url': openapi.Schema(type=openapi.TYPE_STRING),
                                    'previous_url': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        }
                    )
                ),
                400: "Invalid pagination parameters",
                404: "File not found",
                500: "Server error"
            },
            operation_description="List all files in the R2 bucket with pagination support. "
                                "Supports both page/size and limit/offset pagination styles."
        )
    def get(self, request, *args, **kwargs):
        """
        Optimized list of files in the R2 bucket with server-side caching
        """
        start_time = time.time()
        file_name = request.query_params.get('file_name')
        
        try:
            self._validate_config()
            
            if file_name:
                # Single file request - cache the HEAD response metadata (not the object)
                cache_key = f"file_head_{file_name}"
                head_metadata = cache.get(cache_key)
                
                if not head_metadata:
                    s3_client = self._get_r2_client()
                    head_response = s3_client.head_object(
                        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                        Key=file_name
                    )
                    head_metadata = {
                        'ContentLength': head_response['ContentLength'],
                        'LastModified': head_response['LastModified'].isoformat(),
                        'ContentType': head_response['ContentType']
                    }
                    cache.set(cache_key, head_metadata, timeout=self.CACHE_TIMEOUT)
                
                return Response(
                    {
                        'file_name': file_name,
                        'url': self._get_file_url(file_name),
                        'metadata': head_metadata
                    },
                    status=status.HTTP_200_OK
                )
            else:
                # List files with pagination
                try:
                    pagination_params = self._get_pagination_params(request)
                except ValueError as e:
                    return Response(
                        {'error': str(e)},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Get files from cache or R2
                files, last_updated = self._get_cached_file_list()
                total_items = len(files)
                
                # Apply pagination
                paginated_items = files[
                    pagination_params['offset']:pagination_params['offset'] + pagination_params['limit']
                ]
                
                # Build response data
                response_data = []
                for obj in paginated_items:
                    response_data.append({
                        'name': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'],
                        'url': self._get_file_url(obj['Key'])
                    })
                
                # Calculate total pages
                total_pages = math.ceil(total_items / pagination_params['size']) if pagination_params['size'] > 0 else 1
                
                # Build next and previous URLs
                next_url = None
                previous_url = None
                
                if pagination_params['using_page_size']:
                    if pagination_params['page'] < total_pages:
                        next_url = self._build_pagination_url(
                            request,
                            page=pagination_params['page'] + 1
                        )
                    if pagination_params['page'] > 1:
                        previous_url = self._build_pagination_url(
                            request,
                            page=pagination_params['page'] - 1
                        )
                else:
                    if pagination_params['offset'] + pagination_params['limit'] < total_items:
                        next_url = self._build_pagination_url(
                            request,
                            offset=pagination_params['offset'] + pagination_params['limit']
                        )
                    if pagination_params['offset'] > 0:
                        previous_offset = max(0, pagination_params['offset'] - pagination_params['limit'])
                        previous_url = self._build_pagination_url(
                            request,
                            offset=previous_offset
                        )
                
                response = {
                    'files': response_data,
                    'pagination': {
                        'total_items': total_items,
                        'total_pages': total_pages,
                        'current_page': pagination_params['page'],
                        'page_size': pagination_params['size'],
                        'limit': pagination_params['limit'],
                        'offset': pagination_params['offset'],
                        'has_next': (pagination_params['offset'] + pagination_params['limit']) < total_items,
                        'has_previous': pagination_params['offset'] > 0,
                        'next_url': next_url,
                        'previous_url': previous_url,
                        # 'cache_hit': time.time() - last_updated < 60  # Indicate if data was recently cached
                    },
                    # 'response_time_ms': (time.time() - start_time) * 1000
                }
                
                return Response(response, status=status.HTTP_200_OK)
                
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return Response(
                    {'error': 'File not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            logger.error(f"Error accessing R2: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response(
                {'error': 'An unexpected error occurred'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['file'],
                properties={
                    'file': openapi.Schema(
                        type=openapi.TYPE_FILE,
                        description="File to upload"
                    ),
                    'name': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Optional custom filename"
                    )
                }
            ),
            responses={
                201: openapi.Response(
                    description="File uploaded successfully",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'message': openapi.Schema(type=openapi.TYPE_STRING),
                            'file_name': openapi.Schema(type=openapi.TYPE_STRING),
                            'url': openapi.Schema(type=openapi.TYPE_STRING)
                        }
                    )
                ),
                400: "No file provided",
                500: "Server error"
            },
            operation_description="Upload a file to R2 storage bucket. Invalidates cache for the bucket listing."
        )
    def post(self, request, *args, **kwargs):
        """Upload a file to R2 bucket with cache invalidation"""
        try:
            self._validate_config()
            
            if 'file' not in request.FILES:
                return Response(
                    {'error': 'No file provided'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            file_obj = request.FILES['file']
            file_name = request.data.get('name', file_obj.name)
            
            s3_client = self._get_r2_client()
            s3_client.upload_fileobj(
                file_obj,
                settings.AWS_STORAGE_BUCKET_NAME,
                file_name,
                ExtraArgs={
                    'ContentType': file_obj.content_type,
                    'CacheControl': 'max-age=86400'
                }
            )
            
            # Invalidate relevant cache entries
            cache.delete(f"bucket_contents_{settings.AWS_STORAGE_BUCKET_NAME}")
            cache.delete(f"file_head_{file_name}")
            cache.delete(f"file_url_{file_name}")
            
             # Invalidate all relevant caches
            self._invalidate_cache()
            
            return Response(
                {
                    'message': 'File uploaded successfully',
                    'file_name': file_name,
                    'url': self._get_file_url(file_name)
                },
                status=status.HTTP_201_CREATED
            )
            
        except ClientError as e:
            logger.error(f"Error uploading file to R2: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return Response(
                {'error': 'An unexpected error occurred'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'file_name',
                openapi.IN_QUERY,
                description="Name of the file to delete",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="File deleted successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: "Missing file_name parameter",
            500: "Server error"
        },
        operation_description="Delete a file from R2 storage bucket. Invalidates cache for the bucket listing."
    )
    def delete(self, request, *args, **kwargs):
        file_name = request.query_params.get('file_name')
        if not file_name:
            return Response(
                {'error': 'file_name parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            self._validate_config()
            s3_client = self._get_r2_client()
            s3_client.delete_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=file_name
            )
            
            # Invalidate all relevant caches
            self._invalidate_cache()
            
            return Response(
                {'message': f'File {file_name} deleted successfully'},
                status=status.HTTP_200_OK
            )
        except ClientError as e:
            logger.error(f"Error deleting file from R2: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            