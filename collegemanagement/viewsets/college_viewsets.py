from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import College
from ..serializers.college_serializers import CollegeListSerializers, CollegeRetrieveSerializers, CollegeWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response
class collegeViewsets(viewsets.ModelViewSet):
    serializer_class = CollegeListSerializers
    # permission_classes = [collegemanagementPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = College.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name', 'established_date', 'website_link', 'address', 'district', 'phone_number', 'email', 'affiliated', 'college_type', 'discipline', 'social_media', 'google_map_link', 'latitude', 'longitude', 'about', 'brochure', 'step_counter', 'facilities', 'placement', 'scholarship', 'created_date', 'updated_date']
    ordering_fields = ['id','name', 'established_date', 'website_link', 'address', 'district__name', 'phone_number', 'email', 'latitude', 'longitude', 'about', 'brochure', 'step_counter', 'facilities', 'placement', 'scholarship', 'created_date', 'updated_date']
    
    # ('name', 'established_date', 'website_link', 'address', 'district', 'phone_number', 'email', 'affiliated', 'college_type', 'discipline', 'social_media', 'google_map_link', 'latitude', 'longitude', 'about', 'brochure', 'step_counter', 'facilities', 'placement', 'scholarship', 'created_date', 'updated_date', )

    filterset_fields = {
        'id': ['exact'],
        'college_type': ['exact'],
        'affiliated': ['exact'],
        'established_date': ['exact','gte','lte'],
        'created_date': ['exact','gte','lte'],
        'updated_date': ['exact','gte','lte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CollegeWriteSerializers
        elif self.action == 'retrieve':
            return CollegeRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'], url_path="college-logo")
    def get_dp_image(self, request, pk=None):
        try:
            # Fetch the college by primary key
            college = self.get_object()
        except College.DoesNotExist:
            return Response({"error": "College not found."}, status=404)

        # Check if dp_image exists
        if not college.dp_image:
            return Response({"message": "No display image available for this college."}, status=404)

        # Construct the absolute URL for the dp_image
        dp_image_url = request.build_absolute_uri(college.dp_image.url)

        return Response({"college_name": college.name, "dp_image_url": dp_image_url}, status=200)

