from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Gallery
from ..serializers.gallery_serializers import GalleryListSerializers, GalleryRetrieveSerializers, GalleryWriteSerializers
from ..utilities.importbase import *
from rest_framework.response import Response
from rest_framework import status

class galleryViewsets(viewsets.ModelViewSet):
    serializer_class = GalleryListSerializers
    permission_classes = [galleryPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Gallery.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['-id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GalleryWriteSerializers
        elif self.action == 'retrieve':
            return GalleryRetrieveSerializers
        return super().get_serializer_class()
    
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

