from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CollegeGallery
from ..serializers.collegegallery_serializers import CollegeGalleryListSerializers, CollegeGalleryRetrieveSerializers, CollegeGalleryWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response
from mainproj.permissions import DynamicModelPermission
from rest_framework.permissions import AllowAny

class collegegalleryViewsets(viewsets.ModelViewSet):
    serializer_class = CollegeGalleryListSerializers
    permission_classes = [collegemanagementPermission]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = CollegeGallery.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','college__name']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
        'college': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CollegeGalleryWriteSerializers
        elif self.action == 'retrieve':
            return CollegeGalleryRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="latest_college_images", url_path="latest-images",permission_classes=[AllowAny])
    def latest_college_images(self, request, *args, **kwargs):
        # Retrieve the latest 5 images for each college
        colleges = CollegeGallery.objects.values_list('college', flat=True).distinct()
        latest_images = []

        for college in colleges:
            images = CollegeGallery.objects.filter(college=college).order_by('-created_date')[:5]
            latest_images.extend(images)

        serializer = self.get_serializer(latest_images, many=True)
        return Response(serializer.data)

