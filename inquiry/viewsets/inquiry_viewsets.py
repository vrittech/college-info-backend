from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Inquiry
from ..serializers.inquiry_serializers import InquiryListSerializers, InquiryRetrieveSerializers, InquiryWriteSerializers
from ..utilities.importbase import *
from ..utilities.filter import InquiryFilter
from mainproj.permissions import DynamicModelPermission
from rest_framework.permissions import AllowAny

from rest_framework.decorators import action
from rest_framework.response import Response
from collegemanagement.models import College
from django.db.models import Count

class inquiryViewsets(viewsets.ModelViewSet):
    serializer_class = InquiryListSerializers
    permission_classes = [DynamicModelPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Inquiry.objects.all().order_by('-id')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_class = InquiryFilter
    search_fields = ['id', 'full_name', 'email', 'phone', 'courses__name', 'colleges__name']  # Searchable fields
    ordering_fields = ['id', 'full_name', 'created_at', 'updated_at']  # Orderable fields
    ordering = ['id']  # Default ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InquiryWriteSerializers
        elif self.action == 'retrieve':
            return InquiryRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="Inquiries by Course", url_path="inquiries-count/(?P<college_slug>[^/.]+)",permission_classes=[AllowAny])
    def inquiries_by_course(self, request, college_slug=None, *args, **kwargs):
        # Ensure the college exists
        college = College.objects.filter(slug=college_slug).first()
        if not college:
            return Response({"detail": "College not found."}, status=404)

        # Get inquiries related to this college and group by course
        inquiries = Inquiry.objects.filter(colleges=college)
        
        # Aggregate the count of inquiries for each course
        course_inquiry_count = inquiries.values('courses__name') \
            .annotate(count=Count('courses')) \
            .order_by('courses__name')

        # Prepare the response
        data = []
        for item in course_inquiry_count:
            data.append({
                'course': item['courses__name'],
                'count': item['count']
            })
        
        return Response(data)

