from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CollegeGallery,College
from ..serializers.collegegallery_serializers import CollegeGalleryListSerializers, CollegeGalleryRetrieveSerializers, CollegeGalleryWriteSerializers,CollegeSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response
from mainproj.permissions import DynamicModelPermission
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

class collegegalleryViewsets(viewsets.ModelViewSet):
    serializer_class = CollegeGalleryListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = CollegeGallery.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','college__name']
    ordering_fields = ['id']

    filterset_fields = {
        'id': ['exact'],
        'college': ['exact'],
        'college__slug': ['exact'],
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
    
    @action(detail=False, methods=['get'],permission_classes=[AllowAny], url_path="latest-images/(?P<college_slug>[^/]+)")
    def latest_college_images(self, request, college_slug=None, *args, **kwargs):
        # Fetch the college using slug
        college = get_object_or_404(College, slug=college_slug)

        # Get the latest 5 images of the specified college
        images = CollegeGallery.objects.filter(college=college).order_by('-created_date')[:5]

        # Serialize and return the data
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)
    
    # @action(detail=False, methods=['get'],permission_classes=[AllowAny], url_path="latest/(?P<college_slug>[^/]+)")
    # def latest_college_images(self, request, college_slug=None, *args, **kwargs):
    #     # Fetch the college using slug
    #     college = get_object_or_404(College, slug=college_slug)

    #     # Get the latest 5 images of the specified college
    #     images = CollegeGallery.objects.filter(college=college).order_by('-created_date')[:5]

    #     # Serialize and return the data as a flat array
    #     serializer = CollegeGalleryRetrieveSerializers(images, many=True)
    #     return Response(serializer.data)
    
    @action(detail=False, methods=['get'], name="latest_college_images", url_path="latest-images")
    def latest_college_images(self, request):
        """
        Returns all colleges with their details and a single array of latest 3 image URLs.
        """
        colleges = College.objects.all()
        response_data = []

        for college in colleges:
            latest_images = CollegeGallery.objects.filter(college=college).order_by('-created_date')[:3]

            # Convert images into an array of full URLs
            images_array = [request.build_absolute_uri(image.image.url) for image in latest_images]

            if latest_images:
                college_serializer = CollegeSerializers(college)

                response_data.append({
                    "college": {
                        "id": college.id,
                        "slug": college.slug,
                        "name": college.name,
                        "dp_image": request.build_absolute_uri(college.dp_image.url) if college.dp_image else None,
                        "address": college.address,
                        "latest_images": images_array  # Full URLs of latest images
                    }
                })

        return Response(response_data, status=200)


