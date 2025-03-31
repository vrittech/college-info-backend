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
    ordering = ['-id']  # Default ordering

    def get_queryset(self):
        """Admins see all data, normal users see only their college's data"""
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return queryset  # Superusers get all records
            else:
                return queryset.filter(colleges=self.request.user.college)  # Normal users get their college data only

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InquiryWriteSerializers
        elif self.action == 'retrieve':
            return InquiryRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], name="Inquiries by Course", url_path="inquiries-count(?:/(?P<college_slug>[^/.]+))?", permission_classes=[AllowAny])
    def inquiries_by_course(self, request, college_slug=None, *args, **kwargs):
        """
        Get the count of inquiries grouped by course.
        If college_slug is provided, fetch inquiries for that specific college.
        If not, fetch inquiries across all colleges.
        """
        if college_slug:
            # Ensure the college exists
            college = College.objects.filter(slug=college_slug).first()
            if not college:
                return Response({"detail": "College not found."}, status=404)

            # Filter inquiries by the specific college
            inquiries = Inquiry.objects.filter(colleges=college)
        else:
            # Get inquiries across all colleges
            inquiries = Inquiry.objects.all()

        # Aggregate the count of inquiries for each course
        course_inquiry_count = (
            inquiries.values('courses__abbreviation')
            .annotate(total_inquiries=Count('id'))
            .order_by('courses__abbreviation')
        )

        # Calculate total inquiries count
        total_inquiries = inquiries.count()

        # Prepare the response
        data = [
            {'course_name': item['courses__abbreviation'], 'total_inquiries': item['total_inquiries']}
            for item in course_inquiry_count
        ]

        if not data:
            return Response({"message": "No inquiries found.", "total_inquiries": 0}, status=404)

        return Response({
            "total_inquiries": total_inquiries,
            "courses": data
        }, status=200)

