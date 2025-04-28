from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Course
from ..serializers.course_serializers import CourseListSerializers, CourseRetrieveSerializers, CourseWriteSerializers
from ..utilities.importbase import *
from ..utilities.filter import CourseFilter
from mainproj.permissions import DynamicModelPermission
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from rest_framework.response import Response

class courseViewsets(viewsets.ModelViewSet):
    serializer_class = CourseListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Course.objects.all().order_by('-id')
    lookup_field = "slug"

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id','name', 'abbreviation','slug' ]
    ordering_fields = ['id','name', 'abbreviation' ,'created_date', 'updated_date' ]
    filterset_class= CourseFilter
    # ('name', 'abbreviation', 'duration', 'faculties', 'level', 'discipline', 'description', 'course_shortdescription', 'course_outcome', 'course_curriculum', 'eligibility_criteria', 'image', 'curriculum_file_upload', 'created_date', 'updated_date', )

    # filterset_fields = {
    #     'id': ['exact'],
    #     'name': ['exact'],
    #     'abbreviation': ['exact'],
    #     'duration': ['exact'],
    #     'faculty': ['exact'],
    #     'level': ['exact'],
    #     'affiliation': ['exact'],
    #     'description': ['exact'],
    #     'course_shortdescription': ['exact'],
    #     'course_outcome': ['exact'],
    #     'eligibility_criteria': ['exact'],
    #     'created_date': ['exact','gte','lte'],
    #     'updated_date': ['exact','gte','lte'],
    # }
    
    def get_object(self):
        """
        Override get_object to allow lookup by either 'id' or 'slug'.
        """
        queryset = self.get_queryset()
        lookup_value = self.kwargs.get(self.lookup_field)  # Get lookup value from URL
        if lookup_value.isdigit():  # Check if lookup_value is numeric (ID)
            return get_object_or_404(queryset, id=int(lookup_value))
        return get_object_or_404(queryset, slug=lookup_value)  # Otherwise, lookup by slug

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CourseWriteSerializers
        elif self.action == 'retrieve':
            return CourseRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)   

