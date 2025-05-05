from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Gallery,Album
from ..serializers.gallery_serializers import GalleryListSerializers, GalleryRetrieveSerializers, GalleryWriteSerializers
from ..utilities.importbase import *
from rest_framework.response import Response
from rest_framework import status
from mainproj.permissions import DynamicModelPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

cache_time = 1800  # 15 minutes


class galleryViewsets(viewsets.ModelViewSet):
    serializer_class = GalleryListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Gallery.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','album___name']
    ordering_fields = ['-id']

    filterset_fields = {
        'id': ['exact'],
        'album': ['exact'],
        'is_cover': ['exact'],
        'created_date': ['exact', 'lte', 'gte'],
        'updated_date_time': ['exact', 'lte', 'gte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GalleryWriteSerializers
        elif self.action == 'retrieve':
            return GalleryRetrieveSerializers
        return super().get_serializer_class()
    
    
      # List action caching
    def _list(self, request, *args, **kwargs):
        """Actual list implementation"""
        print("Gallery List - uncached version")
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(cache_time, key_prefix="GalleryList"))
    def _cached_list(self, request, *args, **kwargs):
        """Cached version of list"""
        return self._list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self._cached_list(request, *args, **kwargs)
        return self._list(request, *args, **kwargs)

    # Retrieve action caching
    def _retrieve(self, request, *args, **kwargs):
        """Actual retrieve implementation"""
        print("Gallery Retrieve - uncached version")
        return super().retrieve(request, *args, **kwargs)

    @method_decorator(cache_page(cache_time, key_prefix="GalleryRetrieve"))
    def _cached_retrieve(self, request, *args, **kwargs):
        """Cached version of retrieve"""
        return self._retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self._cached_retrieve(request, *args, **kwargs)
        return self._retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method to return all uploaded images in a single response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        gallery_instances = serializer.save()

        # Format the response to return all created images
        response_data = {
            "album": gallery_instances[0].album.id,  # Album ID is the same for all images
            "images": [
                {
                    "id": instance.id,
                    "image_url": instance.image.url if instance.image else None,
                    "is_cover": instance.is_cover,
                    "created_date": instance.created_date,
                    "created_date_time": instance.created_date_time,
                    "updated_date_time": instance.updated_date_time,
                }
                for instance in gallery_instances
            ]
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)


    @action(detail=False, methods=['get'], name="list_all_albums", url_path="all-albums")
    def list_all_albums(self, request, *args, **kwargs):
        # Get all albums
        albums = Album.objects.all().order_by('-id')

        # Create a list where each album has its cover image or None
        album_data = []
        for album in albums:
            cover = Gallery.objects.filter(album=album, is_cover=True).first()
            album_data.append({
                "album_id": album.id,
                "album_name": album.name,
                "cover_image": cover.image.url if cover and cover.image else None
            })

        # Apply pagination
        page = self.paginate_queryset(album_data)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(album_data)

